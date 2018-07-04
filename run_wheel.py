#!/usr/bin/env python3

__author__ = 'anton'

import evdev
import ev3dev.auto as ev3
import threading
import time

#Helpers
def clamp(n, range):
    """
    Given a number and a range, return the number, or the extreme it is closest to.

    :param n: number
    :return: number
    """
    minn, maxn = range
    return max(min(maxn, n), minn)


def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.

    val: float or int
    src: tuple
    dst: tuple

    example: print scale(99, (0.0, 99.0), (-1.0, +1.0))
    """
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

def scalestick(value):
    return scale(value,(0,255),(-100,100))

print("Finding ps3 controller...")
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    if device.name == 'PLAYSTATION(R)3 Controller':
        ps3dev = device.fn


gamepad = evdev.InputDevice(ps3dev)



side_speed = 0
turn_speed = 0
fwd_speed = 0
running = True

class MotorThread(threading.Thread):
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.steer_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.steer_motor.position = 0
        self.gyro = ev3.GyroSensor(ev3.INPUT_4)
        self.gyro.mode = ev3.GyroSensor.MODE_GYRO_RATE
        self.offset = 0
        for i in range(60):
            self.offset += self.gyro.rate
            time.sleep(0.015)
        self.offset /= 100
        threading.Thread.__init__(self)

    def run(self):
        print("Engines running!")
        while running:
            rate = self.gyro.rate - self.offset
            steer_motor_target = (side_speed * fwd_speed / 30.0)
            steer_motor_error = self.steer_motor.position - steer_motor_target
            left_motor_speed = clamp((fwd_speed + side_speed/3)*6.5 + rate*2, (-650,650))
            right_motor_speed = clamp((fwd_speed - side_speed/3)*6.5 + rate*2, (-650,650))
            self.left_motor.run_forever(speed_sp=left_motor_speed)
            self.right_motor.run_forever(speed_sp=right_motor_speed)
            self.steer_motor.run_forever(speed_sp=steer_motor_error * -2)
            # print(steer_motor_error, rate)
            time.sleep(0.015)
        self.left_motor.stop()
        self.right_motor.stop()
        self.steer_motor.stop()


if __name__ == "__main__":
    motor_thread = MotorThread()
    motor_thread.setDaemon(True)
    motor_thread.start()

    for event in gamepad.read_loop(): #this loops infinitely
        if event.type == 3: #A stick is moved

            if event.code == 2: #X axis on right stick
                side_speed = scalestick(event.value)

            if event.code == 5: #Y axis on right stick
                fwd_speed = scalestick(event.value)


        if event.type == 1 and event.code == 302 and event.value == 1:
            print("X button is pressed. Break.")
            running = False
            time.sleep(1) # Wait for the motor thread to finish
            break


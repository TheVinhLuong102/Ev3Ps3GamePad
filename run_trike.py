#!/usr/bin/env python3

__author__ = 'Anton Vanhoucke'

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



side_input = 0
turn_speed = 0
fwd_input = 0
running = True

class MotorThread(threading.Thread):
    def __init__(self):
        self.steer_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.drive_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        threading.Thread.__init__(self)

        # Calibrate
        touch_sensor = ev3.TouchSensor(ev3.INPUT_1)
        while not touch_sensor.is_pressed:
            self.steer_motor.run_forever(speed_sp=-100)
        self.steer_motor.position = -20
        self.steer_motor.stop()

    def run(self):
        global fwd_input
        print("Engines running!")
        while running:
            steer_error = side_input - self.steer_motor.position
            self.steer_motor.run_forever(speed_sp=steer_error*2)
            if -50 < fwd_input < 50: fwd_input = 0  #deadzone 
            self.drive_motor.run_forever(speed_sp=fwd_input)

        self.steer_motor.stop()
        self.drive_motor.stop()


if __name__ == "__main__":
    motor_thread = MotorThread()
    motor_thread.setDaemon(True)
    motor_thread.start()

    for event in gamepad.read_loop(): #this loops infinitely
        if event.type == 3: #A stick is moved

            if event.code == 2: #X axis on right stick
                side_input = scale(event.value,(0,255),(-90,90))

            if event.code == 1: #Y axis on left stick
                fwd_input = scale(event.value,(0,255),(-800,800))


        if event.type == 1 and event.code == 300 and event.value == 1:
            print("Triangle button is pressed. Break.")
            running = False
            time.sleep(0.5) # Wait for the motor thread to finish
            break


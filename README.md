# Ev3Ps3GamePad
Remote control Lego Mindstorms Ev3 Robot with A PS3 sixaxis 
dualoshock 3 gamepad. There are currently two file, one for r
unning a simple tank-type robot, one for a 4-wheel omnibot 
(i.e.) a robot with 4 rotocaster wheels.

# Video
https://www.youtube.com/watch?v=AReDOM4fdA0

# Requirements
LEGO Ev3 brick with ev3dev (http://www.ev3dev.org/)

# Installation
Pair instructions for the gamepad are here:
http://www.ev3dev.org/docs/tutorials/using-ps3-sixaxis/

Type this via ssh on your brick to download and install the code.

```
git clone https://github.com/antonvh/Ev3Ps3GamePad
sudo chmod +x Ev3Ps3GamePad/run_omnibot.py
sudo chmod +x Ev3Ps3GamePad/run_tank.py
```

#Running
After you chmod +x the files, you can run them from your Ev3 brick 
display via file manager. 

#!/bin/bash

clear 

echo "Connecting joystick"

./bluetooth-connect.symlink

python3 main.py --init=true
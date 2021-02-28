#!/bin/sh

rm -f /tmp/.X0-lock
Xvfb :0 -ac &
export DISPLAY=:0
python3 /claimer.py
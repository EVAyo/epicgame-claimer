#!/bin/sh

Xvfb :0 -ac &
export DISPLAY=:0
python3 /claimer.py
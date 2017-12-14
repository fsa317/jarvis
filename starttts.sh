#!/bin/sh
# this script is started via /etc/rc.local
cd /home/pi/tts
python3 mqtts.py > out.log 2> out.err 


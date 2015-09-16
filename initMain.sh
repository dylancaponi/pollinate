#!/bin/sh
until python /media/usb/pollinate/main.py; do
	echo "bee counter crashed with exit code $?  Respawning" >&2
	sleep 1
done

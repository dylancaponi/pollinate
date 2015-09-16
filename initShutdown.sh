#!/bin/sh
until sudo python /media/usb/pollinate/shutdown.py; do
	echo "shutdown.py crashed with exit code $?  Respawning" >&2
	sleep 1
done

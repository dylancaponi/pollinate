#!/bin/bash
echo 'pulling from github'
cd /media/usb/pollinate
git pull >> pullFail.log 2>&1

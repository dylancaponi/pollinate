import RPi.GPIO as GPIO
import time, os


GPIO.setmode(GPIO.BCM)
gpio_pin_number = 23
GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


try:
	GPIO.wait_for_edge(gpio_pin_number, GPIO.RISING)
	os.system("echo Shut down button triggered")
	os.system("sudo shutdown -h now")
except:
	pass

GPIO.cleanup()

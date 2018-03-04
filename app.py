#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from bretpi import addNewTime, startLoop

BtnPin = 12    # pin12 --- button

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buttonCallback(ev=None):
    addNewTime()
    print "button!"

def loop():
    GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=buttonCallback, bouncetime=350)
    while True:
        time.sleep(1)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        startLoop()
        loop()
    except KeyboardInterrupt:
        destroy()

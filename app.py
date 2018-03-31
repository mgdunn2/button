#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from bretpi import addNewTime, startSendLoop

BtnPin = 12

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buttonCallback(ev=None):
    time.sleep(0.08)
    if GPIO.input(BtnPin) != GPIO.LOW:
        return
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
        startSendLoop()
        loop()
    except KeyboardInterrupt:
        destroy()

#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from bretpi import addTime, startLoop

BtnPin = 12    # pin12 --- button

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)

def swLed(ev=None):
    addTime()
    print "button!"

def loop():
    GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=swLed, bouncetime=350) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
    while True:
        time.sleep(1)   # Don't do anything

def destroy():
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        startLoop()
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

import cv2
import numpy as np
import RPi.GPIO as GPIO
import wiringpi
​
import time
import sys


# Sonic sensor echo/trigger GPIOs
SONIC_ECHO_GPIO = 24
SONIC_TRIG_GPIO = 23
def setupGpio():
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(SONIC_ECHO_GPIO, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(SONIC_TRIG_GPIO, wiringpi.GPIO.OUTPUT)

def tryMesure():
    wiringpi.digitalWrite(SONIC_TRIG_GPIO, 1)
    time.sleep(0.00001)
    wiringpi.digitalWrite(SONIC_TRIG_GPIO, 0)

    # save StartTime
    while wiringpi.digitalRead(SONIC_ECHO_GPIO) == 0:
        StartTime = time.time()

    # save time of arrival
    while wiringpi.digitalRead(SONIC_ECHO_GPIO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance

if __name__ == '__main__':
    setupGpio()

    while True:
        dist = tryMesure()
        print("Measured Distance = %.1f cm" % dist)
        time.sleep(1)
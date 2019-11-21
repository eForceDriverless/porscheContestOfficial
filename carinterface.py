import cv2
import numpy as np
import RPi.GPIO as GPIO
import wiringpi

import time
import sys

MIN_ANGLE = 60
MAX_ANGLE = 140

MAX_SPEED = 1000
DIR_FORWARD=0
DIR_BACKWARD=1

# Motor supply enable
MOTOR_SPL_EN_GPIO = 10

# DC motor PWM GPIO
MOTOR_PWM_GPIO = 12

# DC motor direction GPIO
MOTOR_DIR_GPIO = 6

# DC motor disable GPIO
MOTOR_DISABLE_GPIO = 19

# Servo motor PWM GPIO
SERVO_PWM_GPIO = 13

# Sonic sensor echo/trigger GPIOs
SONIC_ECHO_GPIO = 24
SONIC_TRIG_GPIO = 23

# LED GPIO
LED_GPIO = 4

# Switch GPIO
SW_GPIO = 26

def motorInit():
    wiringpi.pwmWrite(MOTOR_PWM_GPIO, 0)
    wiringpi.digitalWrite(MOTOR_SPL_EN_GPIO, 1)
    wiringpi.digitalWrite(MOTOR_DISABLE_GPIO, 0)

def gpioInit():
    # Setup GPIOs
    wiringpi.wiringPiSetupGpio()
    
    wiringpi.pinMode(LED_GPIO, wiringpi.GPIO.OUTPUT)
    wiringpi.digitalWrite(LED_GPIO, wiringpi.GPIO.OUTPUT)
    
    wiringpi.pinMode(MOTOR_SPL_EN_GPIO, wiringpi.GPIO.OUTPUT)
    
    wiringpi.pinMode(MOTOR_DIR_GPIO, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(MOTOR_DISABLE_GPIO, wiringpi.GPIO.OUTPUT)
    
    wiringpi.pinMode(MOTOR_PWM_GPIO, wiringpi.GPIO.PWM_OUTPUT)
    wiringpi.pinMode(SERVO_PWM_GPIO, wiringpi.GPIO.PWM_OUTPUT)
    
    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
    wiringpi.pwmSetClock(192)
    wiringpi.pwmSetRange(2000)
    
    wiringpi.pinMode(SONIC_ECHO_GPIO, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(SONIC_TRIG_GPIO, wiringpi.GPIO.OUTPUT)
    
    GPIO.setmode(GPIO.BCM)

def steer(angle):
    if(angle<MIN_ANGLE):
        angle=MIN_ANGLE
    if(angle>MAX_ANGLE):
        angle=MAX_ANGLE
    wiringpi.pwmWrite(SERVO_PWM_GPIO, int(angle))

def drive(speedReq):
    if(speedReq<-1): speedReq=-1
    else:
        if(speedReq>1): speedReq=1
    if(speedReq<0):
        speedReq=-speedReq
        wiringpi.digitalWrite(MOTOR_DIR_GPIO, DIR_BACKWARD)
    else:
        wiringpi.digitalWrite(MOTOR_DIR_GPIO, DIR_FORWARD)

    wiringpi.pwmWrite(MOTOR_PWM_GPIO,int(MAX_SPEED*speedReq))
	
def getDistanceUS():
    wiringpi.digitalWrite(SONIC_TRIG_GPIO, 1)
    time.sleep(0.00001)
    wiringpi.digitalWrite(SONIC_TRIG_GPIO, 0)
    
    # save StartTime
    StartTime = time.time()
    while wiringpi.digitalRead(SONIC_ECHO_GPIO) == 0:
        StartTime = time.time()

    timeOut = StartTime+0.005
    StopTime = time.time()
    while wiringpi.digitalRead(SONIC_ECHO_GPIO) == 1:
        if(time.time()>timeOut): return -1
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance
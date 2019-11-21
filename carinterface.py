import cv2
import numpy as np
import RPi.GPIO as GPIO
import wiringpi

import time
import sys

MIN_ANGLE = 60
MAX_ANGLE = 140
STEERING_CORRECTION=-10

SPEED = 300

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

def Car_Init():
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
	# GPIO.setup(SW_GPIO, GPIO.IN)
	#GPIO.add_event_detect(SW_GPIO, GPIO.FALLING, button_pressed, 200)
	

def Car_Enable():
	wiringpi.pwmWrite(MOTOR_PWM_GPIO, 0)
    wiringpi.digitalWrite(MOTOR_SPL_EN_GPIO, 1)
    wiringpi.digitalWrite(MOTOR_DISABLE_GPIO, 0)

def Steering(Angle):
	ANG=Angle + (MAX_ANGLE-MIN_ANGLE)/2+STEERING_CORRECTION
	if(ANG<MIN_ANGLE):
		ANG=MIN_ANGLE
	if(ANG>MAX_ANGLE):
		ANG=MAX_ANGLE
	wiringpi.pwmWrite(SERVO_PWM_GPIO, ANG)
	
def US_Get():
	

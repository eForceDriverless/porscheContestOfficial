from carinterface import *
import time

if __name__ == "__main__":
    gpioInit()
    motorInit()

    # test speed
    for i in range(-10, 10, 1):
        speed = i / 10
        drive(i)
        time.sleep(1.5)

    drive(0)
    # test angle
    for a in range(-30, 30, 1):
        steer(90+a)
        time.sleep(0.2)
    steer(90)

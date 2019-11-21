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

    # test angle
    for a in range(-30, 30, 0.1):
        steer(90+a)
        time.sleep(0.1)

import carinterface as CI
import time

CI.gpioInit()
CI.motorInit()


while(1):
        print(CI.getDistanceUS())
        time.sleep(1)
	
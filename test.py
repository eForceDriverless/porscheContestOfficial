import carinterface as CI

CI.gpioInit()
CI.motorInit()

for angle in range(MIN_ANGLE, MAX_ANGLE, 1):
    CI.steer(angle)
    time.sleep(0.05)
    
for angle in range(MAX_ANGLE, MIN_ANGLE, -1):
    CI.steer(angle)
    time.sleep(0.05)

CI.steer(90)
while(1):
	if(CI.getDistanceUS()>20):
		carinterface.drive(0.3)
	else:
		carinterface.drive(0)
	

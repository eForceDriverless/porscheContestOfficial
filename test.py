import carinterface as CI
import time

CI.gpioInit()
CI.motorInit()

CI.drive(0.2)

MIN_ANGLE = 60
MAX_ANGLE = 140
"""
print("going right")
for angle in range(MIN_ANGLE, MAX_ANGLE, 1):
    CI.steer(angle)
    time.sleep(0.05)
    
print("going left")
for angle in range(MAX_ANGLE, MIN_ANGLE, -1):
    CI.steer(angle)
    time.sleep(0.05)
"""
print("center")
CI.steer(90)

print("sonic test")
timeOut = time.time()+100
while(time.time()<timeOut):
    distance = CI.getDistanceUS()
    #print(distance)
    if(distance>40 or distance==-1):
        CI.drive(0.3)
    else:
        CI.drive(0)
    time.sleep(0.5)
CI.drive(0)

#Import modules
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

from lane_detection import detect_lane, display_lines
from heading import compute_steering_angle, stabilize_steering_angle, display_heading_line
from carinterface import steer, drive, motorInit, gpioInit, getDistanceUS

#Initialize camera
camera = PiCamera()
camera.resolution = (320, 240)
camera.color_effects = (128, 128)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
gpioInit()
motorInit()
#Let camera warm up
time.sleep(0.2)

curr_angle = 90
new_angle = 90
startTime = time.time()
i = 0
stop = False
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    if time.time() - startTime > 0.5:
        distance = getDistanceUS()
        startTime = time.time()
        if (distance > 40 or distance == -1):
            drive(0.3)
        else:
            drive(0)
            stop = True
    else:
        if(abs(curr_angle - 90) < 4):
            drive(0.6)
        else:
            drive(0.35)
    img = np.array(frame.array, dtype=np.uint8)
    # cv2.imshow("Preview", img)

    lane_lines = detect_lane(img)
    new_angle = compute_steering_angle(img, lane_lines)

    angle = stabilize_steering_angle(curr_angle, new_angle, len(lane_lines), 5, 4)

    angle = max(65, angle)
    angle = min(115, angle)

    #print("angle", angle)

    curr_angle = angle

    lane_lines_image = display_lines(img, lane_lines)
    heading_image = display_heading_line(img, compute_steering_angle(img, lane_lines))



    drive(0.3)
    steer(angle)

    # if i % 10 == 0:
    #     cv2.imwrite(f"lane_lines_{i}.jpg", lane_lines_image)
    #     cv2.imwrite(f"heading_{i}.jpg", heading_image)

    #cv2.imshow("Stream", lane_lines_image)
    key = cv2.waitKey(1)
    if key == 27 or key == 113:
         cv2.destroyAllWindows()
         drive(0)
         break

    # print(len(lane_lines))
    # lane_lines_image = display_lines(frame, lane_lines)
    # cv2.imshow("lane lines", lane_lines_image)
    rawCapture.truncate(0)
    i += 1
	# key = cv2.waitKey(1)
	# if key == ord("q"):
	# 	print("Quitting")
	# 	break
	
	
# cv2.destroyAllWindows()
camera.close()


#Import modules
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

from lane_detection import detect_lane, display_lines
from heading import compute_steering_angle, stabilize_steering_angle, display_heading_line

#Initialize camera
camera = PiCamera()
camera.resolution = (320, 240)
camera.color_effects = (128, 128)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

#Let camera warm up
time.sleep(0.2)

curr_angle = 90
new_angle = 90

i = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = np.array(frame.array, dtype=np.uint8)
    # cv2.imshow("Preview", img)

    lane_lines = detect_lane(img)
    new_angle = compute_steering_angle(img, lane_lines)

    angle = stabilize_steering_angle(curr_angle, new_angle, len(lane_lines))
    curr_angle = angle

    lane_lines_image = display_lines(img, lane_lines)
    heading_image = display_heading_line(img, compute_steering_angle(img, lane_lines))
    cv2.imwrite(f"lane_lines_{i}.jpg", lane_lines_image)
    cv2.imwrite(f"heading_{i}.jpg", heading_image)

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

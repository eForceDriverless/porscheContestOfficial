import cv2
import numpy as np
from lane_detection import detect_lane, detect_edges, region_of_interest

def display_lines(frame, lines, line_color=(0, 255, 0), line_width=2):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image


# edges = detect_edges(frame)
# cv2.imshow("edges", edges)
# cv2.waitKey(0)


# cropped = region_of_interest(edges)
# cv2.imshow("edges", cropped)
# cv2.waitKey(0)



# cv2.destroyAllWindows()
frame = cv2.imread('test2.jpg')
frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_AREA)

lane_lines = detect_lane(frame)
print(len(lane_lines))
lane_lines_image = display_lines(frame, lane_lines)
cv2.imshow("lane lines", lane_lines_image)
cv2.waitKey(0)

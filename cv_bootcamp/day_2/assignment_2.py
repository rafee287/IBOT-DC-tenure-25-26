import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

image = cv2.imread("circles.png")
result = image.copy()

noisy_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(noisy_gray,5)

circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,dp =1, minDist = 50,
                           param1 = 50, param2=30, minRadius = 5,maxRadius = 100)
h,w = image.shape[:2]

if circles is not None:
    circles = np.uint16(np.around(circles))
    #max = 0
    for circle in circles[0,:] :
        cx, cy, rad = circle
        #if cy > max: max = cy
        # drawing meaningful circles
        if cy < h-20 and cx < w -20: 
            cv2.circle(result,(cx,cy),rad,(0,255,0),2)
            cv2.circle(result, (cx, cy), 2, (0, 0, 255), 2)
#print(max)
cv2.imshow("circles",result)
cv2.waitKey(0)
cv2.destroyAllWindows()






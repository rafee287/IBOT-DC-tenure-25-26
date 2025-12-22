import numpy as np
import cv2

#image processing pipeline 

image = cv2.imread("akaza.jpg")
(h,w,c) = np.shape(image)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# gaussian blur 
blur = cv2.GaussianBlur(gray,(7,7),0)

# Canny edge detection 
edges = cv2.Canny(blur,threshold1 = 50, threshold2 = 150) 

# binary thresholding
_,binary_thresh  = cv2.threshold(edges,127,255,cv2.THRESH_BINARY_INV)

# blur_out = blur.reshape(h,w,3)
# edges_out = edges.reshape(h,w,3)
# binary_thresh_out = binary_thresh.reshape(h,w,3)
blur_out = cv2.cvtColor(blur,cv2.COLOR_GRAY2BGR)
edges_out = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
binary_thresh_out = cv2.cvtColor(binary_thresh,cv2.COLOR_GRAY2BGR)

h_stack_1 = np.hstack((edges_out,binary_thresh_out))
h_stack_2 = np.hstack((image,blur_out))

out = np.vstack((h_stack_2,h_stack_1))

cv2.imshow("out",out)
cv2.waitKey(0)
cv2.destroyAllWindows()
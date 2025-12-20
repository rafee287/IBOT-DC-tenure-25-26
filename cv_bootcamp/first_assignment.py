# Pencil sketch effect 

import numpy as np
import cv2

# image loaded in grayscale format 
gray_image = cv2.imread('akaza.png',cv2.IMREAD_GRAYSCALE)         

if gray_image is None:
    print("error : image not loaded")
else :
    print(f"image loaded : {gray_image.shape}")

cv2.imwrite('1st.jpg',gray_image)

# image inverted 
inverted = 255 - gray_image
cv2.imwrite('2nd.jpg',inverted)

# applied gaussian blur 
gauss_blurred = cv2.GaussianBlur(inverted,(21,21),0)
cv2.imwrite('3rd.jpg',gauss_blurred)

# inverted result 
inverted_blur = 255 - gauss_blurred
cv2.imwrite('4th.jpg',inverted_blur)

# dividing and scaling
sketch = (gray_image/inverted_blur) * 256
cv2.imwrite('5th.jpg',sketch)

clipped = np.clip(sketch,0,255)

cv2.imwrite('final_output.jpg',clipped)
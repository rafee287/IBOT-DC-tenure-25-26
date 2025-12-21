import cv2
import numpy as np

# Load color image
img = cv2.imread("akaza.jpg")

# Split into channels
b, g, r = cv2.split(img)

# Apply pencil sketch to each channel separately
# pencilSketch returns (gray, color), but since we feed single-channel,
# we only use the gray output
sketch_b, _ = cv2.pencilSketch(cv2.merge([b,b,b]), sigma_s=60, sigma_r=0.07, shade_factor=0.04)
sketch_g, _ = cv2.pencilSketch(cv2.merge([g,g,g]), sigma_s=60, sigma_r=0.07, shade_factor=0.04)
sketch_r, _ = cv2.pencilSketch(cv2.merge([r,r,r]), sigma_s=60, sigma_r=0.07, shade_factor=0.04)

# Merge back into a color image
colored_sketch = cv2.merge([sketch_b, sketch_g, sketch_r])

# Save and show
cv2.imwrite("true_colored_sketch.jpg", colored_sketch)
cv2.imshow("True Colored Sketch", colored_sketch)
cv2.waitKey(0)
cv2.destroyAllWindows()
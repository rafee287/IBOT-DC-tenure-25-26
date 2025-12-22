# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# #loading grayscale image
# image = cv2.imread("hooman.png",cv2.IMREAD_GRAYSCALE)
# print(image.shape)

# #histogram 
# hist = cv2.calcHist([image], [0], None, [256], [0,256])

# # Plot histogram
# plt.plot(hist, color='black')
# plt.title("Grayscale Histogram")
# plt.xlabel("Pixel Intensity")
# plt.ylabel("Frequency")
# plt.savefig("histogram.jpg")

# histogram = cv2.imread("histogram.jpg",cv2.IMREAD_GRAYSCALE) 
# print(histogram.shape)
# # statistics mean and standard deviation
# mean, stdev = cv2.meanStdDev(image)
# median = np.median(image)

# print("Mean intensity:", mean[0][0])
# print("Median intensity", median)
# print("Standard deviation:", stdev[0][0])

# # Pad img2 to match img1's size
# diff_height = image.shape[0] -histogram.shape[0] 
# print(diff_height)
# diff_width  = -histogram.shape[1] + image.shape[1] 
# print(diff_width)

# # computing even padding
# top    = diff_height // 2
# bottom = diff_height - top
# left   = diff_width // 2
# right  = diff_width - left

# image_padded = cv2.copyMakeBorder(
#     histogram,
#     top , bottom , left, right,
#     cv2.BORDER_CONSTANT, value=(0,0,0)  # black padding
# )

# out = np.hstack((image_padded,histogram))
# cv2.imshow("out",out)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


import cv2
import numpy as np
import matplotlib.pyplot as plt

# loading grayscale image
image = cv2.imread("akaza.jpg", cv2.IMREAD_GRAYSCALE)
print(image.shape)

# histogram
hist = cv2.calcHist([image], [0], None, [256], [0,256])
plt.plot(hist, color='black')
plt.title("Grayscale Histogram")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")
plt.savefig("histogram.jpg")

# load histogram image
histogram = cv2.imread("histogram.jpg", cv2.IMREAD_GRAYSCALE)
print(histogram.shape)

# statistics mean and standard deviation
mean, stdev = cv2.meanStdDev(image)
median = np.median(image)

print("Mean intensity:", mean[0][0])
print("Median intensity:", median)
print("Standard deviation:", stdev[0][0])

# resize histogram to match image size 
histogram_resized = cv2.resize(histogram, (image.shape[1], image.shape[0]))

# stack side by side
out = np.hstack((image, histogram_resized))
cv2.imshow("out", out)
cv2.waitKey(0)
cv2.destroyAllWindows()
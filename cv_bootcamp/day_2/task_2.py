import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load images
image1 = cv2.imread("mouse1.png")
image2 = cv2.imread("mouse2.png")

# Create ORB detector
orb = cv2.ORB_create(nfeatures=500)

# Detect and compute descriptors
gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
keypoints1, descriptors1 = orb.detectAndCompute(gray1, None)

gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
keypoints2, descriptors2 = orb.detectAndCompute(gray2, None)

print(f"Image1: {len(keypoints1)} keypoints")
print(f"Image2: {len(keypoints2)} keypoints")

# Match descriptors
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(descriptors1, descriptors2)

# Sort matches by distance
matches = sorted(matches, key=lambda x: x.distance)

# let number of matches to be displayed = 7%
length = int(0.07*len(matches))

# 7% chosen because for my image choice, only at this level scrutinity, i am getting meaningful matches

# Define good matches (the top 20% as per mentioned in the above line)
good_matches = matches[:length]
print(f"Number of good matches: {len(good_matches)}")

# Draw matches
match_img = cv2.drawMatches(image1, keypoints1, image2, keypoints2,
                            good_matches, None,
                            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imwrite("match_image.jpg",match_img)
# Display
plt.imshow(match_img)
plt.title("ORB Keypoint Matches")
plt.show()
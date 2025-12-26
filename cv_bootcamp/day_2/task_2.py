import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# getting an image 
image = cv2.imread("hooman.png")
# creating an ORB object 
orb = cv2.ORB_create(nfeatures = 500)   # detect upto 500 keypoints 

# detect keypoints and compute descriptors 
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
keypoints,descriptors = orb.detectAndCompute(gray,None)

print(f"Found {len(keypoints)} keypoints")
print(f"Deescriptor shape: {descriptors.shape}")

# drawing 
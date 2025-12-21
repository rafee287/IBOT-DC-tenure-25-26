# Pencil sketch effect 

import numpy as np
import cv2

images = ["akaza.jpg","scenery.png","warrior.png"]
output = ["akaza_out.jpg","scenery_out.jpg","warrior_out.jpg"]

for i in range(len(images)):
    actual_image = cv2.imread(images[i])
        
    # image loaded in grayscale format 
    gray_image = cv2.imread(images[i],cv2.IMREAD_GRAYSCALE)         

    if gray_image is None:
        print("error : image not loaded")
    else :
        print(f"image loaded : {gray_image.shape}")

    #cv2.imwrite('1st.jpg',gray_image)

    # image inverted 
    inverted = 255 - gray_image
    #cv2.imwrite('2nd.jpg',inverted)

    # applied gaussian blur 
    gauss_blurred = cv2.GaussianBlur(inverted,(21,21),0)
    #cv2.imwrite('3rd.jpg',gauss_blurred)

    # inverted result 
    inverted_blur = 255 - gauss_blurred
    #cv2.imwrite('4th.jpg',inverted_blur)

    # dividing and scaling
    sketch = cv2.divide(gray_image, inverted_blur, scale=256)
    #used function to avoid divide by zero warnings

    #cv2.imwrite('5th.jpg',sketch)

    clipped = np.clip(sketch,0,255)
    #cv2.imwrite('final_output.jpg',clipped)
    
    #modifying output 
    out = cv2.cvtColor(clipped.astype(np.uint8),cv2.COLOR_GRAY2BGR)

    side_by_side = np.hstack((actual_image,out))

    cv2.imwrite(output[i],side_by_side)

# # Pencil sketch effect 

# import numpy as np
# import cv2

# images = ["akaza.jpg","scenery.png","warrior.png"]
# output = ["akaza_out.jpg","scenery_out.jpg","warrior_out.jpg"]

# for i in range(len(images)):
#     actual_image = cv2.imread(images[2-i])
        
#     # image loaded in grayscale format 
#     gray_image = cv2.imread(images[2-i],cv2.IMREAD_GRAYSCALE)         

#     if gray_image is None:
#         print("error : image not loaded")
#     else :
#         print(f"image loaded : {gray_image.shape}")

#     #cv2.imwrite('1st.jpg',gray_image)

#     equalized = cv2.equalizeHist(gray_image)
#     # cv2.imshow("Equalized", equalized)
#     # cv2.waitKey(0)
    
#     # image inverted 
#     inverted = 255 - gray_image
#     #cv2.imwrite('2nd.jpg',inverted)

#     # applied gaussian blur 
#     gauss_blurred = cv2.GaussianBlur(inverted,(21,21),0)
#     #cv2.imwrite('3rd.jpg',gauss_blurred)

#     # blurred for edges 
#     blurred = cv2.GaussianBlur(gray_image,(5,5),0)
#     edges = 255 - cv2.Canny(equalized,threshold1 =50, threshold2 =150)

#     # cv2.imshow("edges",255-edges)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#     # break
#     # inverted result 
#     inverted_blur = 255 - gauss_blurred
#     #cv2.imwrite('4th.jpg',inverted_blur)

#     # dividing and scaling
#     sketch = cv2.divide(gray_image, inverted_blur, scale=256)
#     #used function to avoid divide by zero warnings

#     #cv2.imwrite('5th.jpg',sketch)

#     clipped = np.clip(sketch,0,255)
#     #cv2.imwrite('final_output.jpg',clipped)
    
#     #modifying output 
#     out = cv2.cvtColor(clipped.astype(np.uint8),cv2.COLOR_GRAY2BGR) + cv2.cvtColor(edges.astype(np.uint8),cv2.COLOR_GRAY2BGR)

#     side_by_side = np.hstack((actual_image,out))

#     cv2.imwrite(output[2-i],side_by_side)

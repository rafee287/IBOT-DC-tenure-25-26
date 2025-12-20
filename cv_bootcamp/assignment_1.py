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


import cv2
import numpy as np

def pencil_sketch(image_path, output_path):
    # Step 1: Read the color image
    color_img = cv2.imread(image_path)
    if color_img is None:
        print("Error: Image not loaded")
        return
    
    # Step 2: Convert to grayscale
    gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

    # Step 3: Equalize histogram (optional, improves contrast)
    #gray_img = cv2.equalizeHist(gray_img)

    # Step 4: Invert grayscale
    inverted = 255 - gray_img

    # Step 5: Apply Gaussian blur to inverted image
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)

    # Step 6: Invert the blurred image
    inverted_blur = 255 - blurred

    # Step 7: Divide grayscale by inverted blur (safe division)
    sketch = cv2.divide(gray_img, inverted_blur, scale=256)

    # Step 8: Convert back to 3-channel for display/merge
    sketch_bgr = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    # Step 9: Side-by-side comparison
    side_by_side = np.hstack((color_img, sketch_bgr))

    # Save result
    cv2.imwrite(output_path, side_by_side)
    print(f"Saved pencil sketch to {output_path}")


# Example usage
pencil_sketch("warrior.png", "warrior_sketch.jpg")
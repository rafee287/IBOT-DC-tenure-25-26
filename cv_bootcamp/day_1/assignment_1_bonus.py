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

    #display result 
    cv2.imshow(output_path,side_by_side)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(f"Saved pencil sketch to {output_path}")

def blur_adjust_pencil_sketch(image_path,output_path,blur,sigma):
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
    blurred = cv2.GaussianBlur(inverted, (blur, blur), sigma)

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

    #display result 
    cv2.imshow(output_path,side_by_side)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(f"Saved pencil sketch to {output_path}")

    return sketch

def color_sketch(image_path,output_path):
    # loaded image
    image = cv2.imread(image_path)
    # gray image
    gray_image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    #pencil_sketch algo
    inverted = 255 - gray_image
    blurred = cv2.GaussianBlur(inverted,(71,71),0)
    inverted_blur = 255-blurred
    sketch = cv2.divide(gray_image,inverted_blur,scale = 256)
    cv2.imshow("sketch.jpg",sketch)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    hsv[...,2] = sketch
    out = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    cv2.imwrite(output_path,out)


# Example usage
#pencil_sketch("akaza.jpg", "akaza_sketch.jpg")
color_sketch("hooman.png", "hooman_color.jpg")
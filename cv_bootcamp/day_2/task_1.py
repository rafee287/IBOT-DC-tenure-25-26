import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


# augmentation pipeline

def augment_from_folder(path):
    # accessing files
    files = os.listdir(path)
    # filtering images
    ims = [f for f in files if f.lower().endswith(('.png','.jpeg','.jpg'))]
    #printing images found 
    print("images_found", ims)
    
    # output folder 
    output_folder = r"C:\Users\rafee\ibot_25-26\IBOT-DC-tenure-25-26\cv_bootcamp\day_2\output"
    #creating the folder if it doesnt exist
    os.makedirs(output_folder,exist_ok = True)

    for j in ims:
        i = cv2.imread(os.path.join(path, j))
        h,w = i.shape[:2]
        # flips
        flipped_horizontally = cv2.flip(i, 1)  # Horizontal flip
        flipped_vertically = cv2.flip(i, 0)    # Vertical flip
        flipped_both = cv2.flip(i, -1)         # Both horizontal and vertical flip

        # rotation 
        centre = (w//2,h//2)
        angle = np.random.uniform(-45,45)
        scale = 1.0
        rotation_matrix = cv2.getRotationMatrix2D(centre, angle, scale)
        rotated_img = cv2.warpAffine(i,rotation_matrix,(w,h))           # rotation matrix applied

        # scaling 
        # zooming in 
        scale_factor = 2
        zoomed_in = cv2.resize(i,None,fx = scale_factor, fy = scale_factor)
        # cropping
        start_y = (zoomed_in.shape[0] - h)//2
        start_x = (zoomed_in.shape[1] - w)//2
        zoom = zoomed_in[start_y:start_y+h,start_x:start_x+w]

        # zooming out
        scale_factor = 0.5
        zoom_out_small = cv2.resize(i, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)
        h, w = i.shape[:2]
        padded = cv2.copyMakeBorder(
            zoom_out_small,
            top=(h - zoom_out_small.shape[0]) // 2,
            bottom=(h - zoom_out_small.shape[0] + 1) // 2,
            left=(w - zoom_out_small.shape[1]) // 2,
            right=(w - zoom_out_small.shape[1] + 1) // 2,
            borderType=cv2.BORDER_CONSTANT,
            value=[0, 0, 0]  # black padding
        )

        # translation (shifting)
        tx,ty = 200,150 
        translation_matrix = np.float32(([1,0,tx],[0,1,0]))
        translated = cv2.warpAffine(i, translation_matrix, (w, h))

        # shearing 
        shear_factor = 0.2
        shear_matrix = np.float32([[1,shear_factor,0],[0,1,0]])
        sheared = cv2.warpAffine(i,shear_matrix,(w,h))

        # creating the output 
        images = {
            "Original": i,
            "Flip Horizontal": flipped_horizontally,
            "Flip Vertical": flipped_vertically,
            "Flip Both": flipped_both,
            "Rotated": rotated_img,
            "Zoom In": zoom,
            "Zoom Out": padded,
            "Translated": translated,
            "Sheared": sheared
        }
        # plotting in a 3x3 grid 
        fig, axes = plt.subplots(3, 3, figsize=(15, 10))

        for ax, (title, img) in zip(axes.flat, images.items()):
            ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            ax.set_title(title)
            ax.axis("off")

        plt.tight_layout()

        #saving the grid of images 
        output_dir = "augmented_results"
        os.makedirs(output_dir, exist_ok=True)
        grid_path = os.path.join(output_dir, f"all_transformations_grid_{ims.index(j)}.jpg")
        
        plt.savefig(grid_path)
        #plt.show()

        print(f"Saved combined grid image to {grid_path}")



# use double back slash as \ is an escape sequence
augment_from_folder("C:\\Users\\rafee\\ibot_25-26\\IBOT-DC-tenure-25-26\\cv_bootcamp\\day_2\\images")

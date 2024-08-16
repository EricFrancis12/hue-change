import numpy as np
import cv2

def process_png(image_path, old_hue, new_hue, output_path):
    # Load the image with alpha channel (RGBA)
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    # Check if the image has an alpha channel
    if image.shape[2] == 4:
        # Split the image into its RGB and alpha channels
        rgb_image = image[:, :, :3]
        alpha_channel = image[:, :, 3]
    else:
        raise ValueError("Image does not have an alpha channel")

    # Convert RGB to HSV
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)

    # Calculate hue shift
    hue_shift = (new_hue - old_hue) % 180

    # Apply hue shift
    hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_shift) % 180

    # Convert back to RGB
    rgb_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # Combine RGB image with alpha channel
    result_image = np.dstack((rgb_image, alpha_channel))

    # Save the result image
    cv2.imwrite(output_path, result_image)

blue_hue = 120  # Example value, adjust according to actual blue hue in the image

for i in range(40):
    red_hue = i * 10
    process_png('image.png', blue_hue, red_hue, f'./png/output-{i}.png')

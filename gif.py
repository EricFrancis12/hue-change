import numpy as np
from PIL import Image

def temp_change_color_scheme(image, old_hue, new_hue):
    # Convert the image to RGBA mode
    image = image.convert('RGBA')
    
    # Convert image to NumPy array
    np_image = np.array(image)
    
    # Split the RGBA channels
    rgb_image = np_image[:, :, :3]
    alpha_channel = np_image[:, :, 3]
    
    # Convert RGB to HSV using PIL
    hsv_image = Image.fromarray(rgb_image, 'RGB').convert('HSV')
    hsv_array = np.array(hsv_image)
    
    # Calculate hue shift
    hue_shift = (new_hue - old_hue) % 360
    
    # Apply hue shift
    hsv_array[:, :, 0] = (hsv_array[:, :, 0] + hue_shift) % 360
    
    # Convert back to RGB
    rgb_image = Image.fromarray(hsv_array, 'HSV').convert('RGB')
    
    # Convert RGB image and alpha channel back to NumPy arrays
    rgb_array = np.array(rgb_image)
    alpha_array = np.array(alpha_channel)
    
    # Combine RGB image with alpha channel
    result_array = np.dstack((rgb_array, alpha_array))
    
    # Convert result back to PIL Image
    result_image = Image.fromarray(result_array, 'RGBA')
    
    return result_image

def process_gif(input_gif_path, output_gif_path, old_hue, new_hue):
    # Open the GIF
    with Image.open(input_gif_path) as img:
        frames = []
        durations = []
        try:
            while True:
                # Process each frame
                frame = img.copy()
                processed_frame = temp_change_color_scheme(frame, old_hue, new_hue)
                frames.append(processed_frame)
                durations.append(img.info['duration'])  # Save duration of each frame
                img.seek(img.tell() + 1)
        except EOFError:
            pass  # End of sequence
    
    # Save the processed frames as a new GIF
    frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=durations,  # Use durations for each frame
        disposal=2  # Set disposal method to "restore to background color"
    )

blue_hue = 120  # Example value, adjust according to actual blue hue in the image

for i in range(40):
    red_hue = i * 10
    process_gif('image.gif', f'./gifs/output-{i}.gif', blue_hue, red_hue)

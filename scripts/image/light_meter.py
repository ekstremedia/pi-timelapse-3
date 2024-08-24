from PIL import Image
import numpy as np

def calculate_light_level(image_path):
    """
    Calculates the average brightness of an image.
    
    Parameters:
        image_path (str): Path to the image file.
        
    Returns:
        float: A value representing the average brightness of the image.
    """
    # Open the image
    with Image.open(image_path) as img:
        # Convert the image to grayscale
        grayscale_img = img.convert("L")
        # Convert the image data to a numpy array
        image_array = np.array(grayscale_img)
        # Calculate the mean brightness
        light_level = np.mean(image_array)
    
    return light_level

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python light_meter.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    light_level = calculate_light_level(image_path)
    print(f"The average light level in the image is: {light_level}")

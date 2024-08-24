import os
import argparse
from light_meter import calculate_light_level

def process_images_in_directory(directory):
    """
    Processes all images in the specified directory and prints their light levels in order.
    
    Parameters:
        directory (str): Path to the directory containing the images.
    """
    # List all image files in the directory and sort them
    image_files = sorted([f for f in os.listdir(directory) if f.endswith('.jpg')])

    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        light_level = calculate_light_level(image_path)
        # Print the light level rounded to one decimal place
        print(f"{image_file}: Light level = {light_level:.1f}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process images in a directory and calculate light levels.")
    parser.add_argument("directory", help="Path to the directory containing the images")
    
    args = parser.parse_args()
    
    # Process images in the provided directory
    process_images_in_directory(args.directory)

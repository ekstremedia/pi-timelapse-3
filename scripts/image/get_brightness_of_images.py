import os
import argparse
import time
from light_meter import calculate_light_level
from calculate_iso_and_shutter import calculate_iso_and_shutter

def process_images_in_directory(directory):
    """
    Processes all images in the specified directory and prints their light levels in order,
    along with the time taken to process each image, the calculated ISO, shutter speed, and daylight status.
    
    Parameters:
        directory (str): Path to the directory containing the images.
    """
    # List all image files in the directory and sort them
    image_files = sorted([f for f in os.listdir(directory) if f.endswith('.jpg')])

    for image_file in image_files:
        image_path = os.path.join(directory, image_file)

        # Start timing
        start_time = time.time()

        light_level = calculate_light_level(image_path)

        # Calculate ISO, shutter speed, and daylight status
        iso, shutter, daylight = calculate_iso_and_shutter(light_level)

        # End timing
        end_time = time.time()

        # Calculate the elapsed time in milliseconds
        elapsed_time = (end_time - start_time) * 1000

        # Print the light level, time taken, ISO, shutter speed, and daylight status
        print(f"{image_file}: Light level = {light_level:.1f} ({elapsed_time:.2f} ms), "
              f"ISO = {iso}, Shutter Speed = {shutter}, Daylight = {daylight}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process images in a directory and calculate light levels.")
    parser.add_argument("directory", help="Path to the directory containing the images")
    
    args = parser.parse_args()
    
    # Process images in the provided directory
    process_images_in_directory(args.directory)

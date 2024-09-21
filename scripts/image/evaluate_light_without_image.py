import os
import json
import time
from picamera2 import Picamera2

# Paths for storing metadata
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
METADATA_FILE = os.path.join(DATA_DIR, 'evaluation_measure.json')

def create_directory_if_not_exists(directory):
    """
    Creates the directory if it doesn't already exist.

    Parameters:
        directory (str): The directory path to create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def evaluate_light_level_without_image():
    """
    Evaluates the light level using the camera sensor without saving an image.
    
    Returns:
        dict: The metadata dictionary including Lux value.
    """
    # Initialize the camera
    picam2 = Picamera2()
    
    # Configure the camera for minimal preview (no need for high resolution)
    preview_config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure("preview")
    
    # Start the camera for a brief period to gather sensor data
    picam2.start()
    time.sleep(1)  # Allow camera to warm up and gather data

    # Capture sensor metadata
    metadata = picam2.capture_metadata()
    
    # Stop the camera
    picam2.stop()

    # Extract the Lux value for display purposes
    lux = metadata.get('Lux', 'N/A') if metadata else 'N/A'
    print(f"Evaluated Lux without image capture: {lux}")
    
    # Return the full metadata dictionary
    return metadata

def save_metadata_to_file(metadata, file_path):
    """
    Saves the metadata to a JSON file.

    Parameters:
        metadata (dict): The metadata to save.
        file_path (str): The file path to save the metadata.
    """
    with open(file_path, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)
    print(f"Metadata saved to {file_path}")

if __name__ == "__main__":
    # Create the data directory if it doesn't exist
    create_directory_if_not_exists(DATA_DIR)

    # Evaluate light level without saving an image
    metadata = evaluate_light_level_without_image()

    # Save the metadata to a JSON file
    save_metadata_to_file(metadata, METADATA_FILE)

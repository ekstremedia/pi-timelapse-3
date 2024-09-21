import os
import time
import yaml
import json
from picamera2 import Picamera2
import libcamera

def load_config(config_path):
    """
    Loads the configuration from a YAML file.

    Parameters:
        config_path (str): Path to the config.yaml file.

    Returns:
        dict: The configuration dictionary.
    """
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def create_directory_if_not_exists(directory):
    """
    Creates the directory if it doesn't already exist.

    Parameters:
        directory (str): The directory path to create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_metadata(metadata, output_path):
    """
    Saves the metadata to a JSON file.

    Parameters:
        metadata (dict): The metadata to save.
        output_path (str): The file path to save the metadata.
    """
    with open(output_path, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)
    print(f"Metadata saved to {output_path}")

def capture_light_valuation_image():
    """
    Captures an image for light valuation using the lores size settings from config.yaml.
    Saves the image to temp/light_valuation.jpg and stores metadata in data/evaluation_measure.json.
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '../../config.yaml')
    config = load_config(config_path)

    # Create the output directory if it doesn't exist
    temp_directory = 'temp'
    create_directory_if_not_exists(temp_directory)
    output_path = os.path.join(temp_directory, 'light_valuation.jpg')

    # Path to save the metadata
    data_directory = os.path.join(os.path.dirname(__file__), '../../data')
    create_directory_if_not_exists(data_directory)
    metadata_output_path = os.path.join(data_directory, 'evaluation_measure.json')

    # Initialize the camera with the lores size
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(
        main={"size": tuple(config['camera_settings']['lores_size'])},  # Set main to lores_size
        lores={"size": tuple(config['camera_settings']['lores_size'])},
        controls={"AfMode": libcamera.controls.AfModeEnum.Manual}  # Assuming manual focus
    )
    picam2.configure(camera_config)

    # Start the camera and capture the image
    picam2.start()
    
    # Capture image and metadata
    request = picam2.capture_request()
    if request is not None:
        request.save("main", output_path)
        metadata = request.get_metadata()  # Retrieve metadata
        request.release()
    else:
        print("Failed to capture image.")
        metadata = {}

    # Stop the camera
    picam2.stop()
    time.sleep(2)

    print(f"Light valuation image saved to {output_path}")

    # Save metadata to JSON file
    save_metadata(metadata, metadata_output_path)

if __name__ == "__main__":
    capture_light_valuation_image()

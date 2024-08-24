from picamera2 import Picamera2
from datetime import datetime
import os
import yaml

def load_config(config_file="config.yaml"):
    """
    Loads the configuration from a YAML file.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def create_output_directory(directory_name):
    """
    Creates the output directory if it doesn't exist.
    """
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    return directory_name

def generate_image_filename(directory, prefix, extension):
    """
    Generates a filename based on the current timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(directory, f"{prefix}_{timestamp}.{extension}")

def capture_image(output_directory, prefix, extension):
    """
    Captures an image and saves it to the specified directory.
    """
    picam2 = Picamera2()
    picam2.start()
    
    image_filename = generate_image_filename(output_directory, prefix, extension)
    picam2.capture_file(image_filename)
    
    picam2.stop()
    print(f"Image saved as {image_filename}")

if __name__ == "__main__":
    config = load_config()
    
    output_directory = create_output_directory(config['output_directory'])
    capture_image(output_directory, config['image_prefix'], config['image_extension'])

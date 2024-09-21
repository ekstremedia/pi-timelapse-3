import subprocess
import sys
import os
import json
from light_meter import calculate_light_level
from calculate_iso_and_shutter import calculate_iso_and_shutter
from datetime import datetime

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from scripts.database.database_store import insert_evaluation  # Correct function name to match your database_store.py


def capture_light_valuation_image():
    """
    Executes the capture_light_valuation_image.py script to capture the light valuation image.
    """
    script_path = os.path.join(os.path.dirname(__file__), 'capture_light_valuation_image.py')
    subprocess.run(['python3', script_path], check=True)
    print("Image capture completed.")


def evaluate_light_level(image_path):
    """
    Evaluates the light level of the given image using the light_meter module.
    
    Parameters:
        image_path (str): Path to the image file to evaluate.
    
    Returns:
        float: The calculated light level.
    """
    light_level = calculate_light_level(image_path)
    print(f"Light level for {image_path}: {light_level:.1f}")
    return light_level


def save_values_to_file(light_level, iso, shutter_speed, file_path='temp/last_measurement.json'):
    """
    Saves the light level, ISO, and shutter speed to a JSON file.
    
    Parameters:
        light_level (float): The measured light level.
        iso (int or str): The calculated ISO value.
        shutter_speed (int or str): The calculated shutter speed in microseconds.
        file_path (str): The file path to save the values.
    """
    data = {
        "light_level": light_level,
        "iso": iso,
        "shutter_speed": shutter_speed
    }
    with open(file_path, 'w') as file:
        json.dump(data, file)
    print(f"Values saved to {file_path}")


def load_values_from_file(file_path='temp/last_measurement.json'):
    """
    Loads the light level, ISO, and shutter speed from a JSON file.
    
    Parameters:
        file_path (str): The file path to load the values from.
    
    Returns:
        tuple: (light_level, iso, shutter_speed)
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data["light_level"], data["iso"], data["shutter_speed"]
    else:
        print(f"No previous measurement found at {file_path}")
        return None, None, None


if __name__ == "__main__":
    # Capture the light valuation image
    capture_light_valuation_image()
    
    # Path to the captured image
    image_path = os.path.join('temp', 'light_valuation.jpg')
    
    # Evaluate the light level of the captured image
    light_level = evaluate_light_level(image_path)
    
    # Load the previously stored evaluation values (from the JSON file)
    metadata_file_path = os.path.join('data', 'evaluation_measure.json')
    with open(metadata_file_path, 'r') as f:
        evaluated_values = json.load(f)

    # Get the relevant metadata (Lux and ExposureTime)
    evaluated_lux = evaluated_values.get("Lux", None)  # If not found, fallback to calculated light level
    evaluated_exposure_time = evaluated_values.get("ExposureTime", None)

    # Get the current datetime
    capture_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    iso, shutter_speed, _ = calculate_iso_and_shutter(light_level)

    # Store Lux, ExposureTime, and datetime in the database
    insert_evaluation(evaluated_lux=evaluated_lux, evaluated_exposure_time=evaluated_exposure_time)

    # Save the values to a JSON file
    save_values_to_file(light_level, iso, shutter_speed)

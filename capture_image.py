import os
import subprocess
import json
from datetime import datetime
import time
from picamera2 import Picamera2
import libcamera
import yaml
from scripts.log.logging import setup_logger, log_message, setup_logging_directory
from scripts.image.calculate_iso_and_shutter import calculate_iso_and_shutter

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

def capture_image(config, iso, shutter_speed, daylight, logger=None):
    """
    Captures an image using the provided ISO and shutter speed settings.

    Parameters:
        config (dict): The configuration dictionary from config.yaml.
        iso (int or str): The ISO setting for the capture.
        shutter_speed (int or str): The shutter speed setting for the capture.
        daylight (bool): Whether it's daylight or not.
        logger (logging.Logger, optional): Logger instance for logging events.
    """
    picam2 = Picamera2()

    # Determine focus mode and lens position based on config
    focus_mode = libcamera.controls.AfModeEnum.Manual if config['camera_settings']['focus_mode'] == 'manual' else libcamera.controls.AfModeEnum.Auto
    lens_position = config['camera_settings']['lens_position'] if config['camera_settings']['focus_mode'] == 'manual' else None

    if daylight:
        # Daytime configuration
        camera_config = picam2.create_still_configuration(
            main={"size": tuple(config['camera_settings']['main_size'])},
            lores={"size": tuple(config['camera_settings']['lores_size'])},
            display=config['camera_settings']['display'],
            controls={
                "AwbEnable": config['camera_settings']['awb_enable'],
                "AwbMode": getattr(libcamera.controls.AwbModeEnum, config['camera_settings']['awb_mode']),
                "AfMode": focus_mode,
                "LensPosition": lens_position,
                "ColourGains": tuple(config['camera_settings']['colour_gains_day']),
                "AnalogueGain": 1  # Default gain for daytime
            }
        )
    else:
        # Nighttime configuration
        camera_config = picam2.create_still_configuration(
            main={"size": tuple(config['camera_settings']['main_size'])},
            lores={"size": tuple(config['camera_settings']['lores_size'])},
            display=config['camera_settings']['display'],
            controls={
                "AwbEnable": config['camera_settings']['awb_enable'],
                "AwbMode": getattr(libcamera.controls.AwbModeEnum, config['camera_settings']['awb_mode']),
                "AfMode": focus_mode,
                "LensPosition": lens_position,
                "ColourGains": tuple(config['camera_settings']['colour_gains_night']),
                "ExposureTime": int(shutter_speed),  # Only set at night
                "AnalogueGain": round(iso)  # Only set at night
            }
        )

    picam2.configure(camera_config)

    # Start the camera and capture the image
    picam2.start()
    time.sleep(2)  # Allow camera to adjust

    now = datetime.now()
    dir_name = os.path.join(config['image_output']['root_folder'], now.strftime(config['image_output']['folder_structure']))
    os.makedirs(dir_name, exist_ok=True)
    file_name = os.path.join(dir_name, f"{config['image_output']['filename_prefix']}{now.strftime('%Y_%m_%d_%H_%M_%S')}.{config['image_output']['image_extension']}")
    
    picam2.capture_file(file_name)
    picam2.stop()

    log_entry = f"Captured image {file_name} with settings: ISO={iso}, Shutter={shutter_speed}, Daylight={daylight}, Config={camera_config['controls']}"
    print(log_entry)

    if logger:
        log_message(logger, log_entry)

    print(f"Image captured and saved to {file_name}")


if __name__ == "__main__":
    # Load the configuration
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    config = load_config(config_path)

    # Setup logging if enabled
    logger = None
    if config.get('logging', {}).get('capture_image', False):
        logs_dir = setup_logging_directory()
        log_file = os.path.join(logs_dir, 'capture_image.log')
        logger = setup_logger('capture_image', log_file)

    # Check if debug mode is enabled in config.yaml
    debug_mode = config.get('debug', {}).get('enabled', False)
    debug_light_level = config.get('debug', {}).get('light_level', None)

    if debug_mode and debug_light_level is not None:
        light_level = debug_light_level
        iso, shutter_speed, _ = calculate_iso_and_shutter(light_level)
        log_message(logger, f"Debug mode enabled. Overriding light level to {light_level}")
    else:
        # Run the light evaluation script
        subprocess.run(['python3', 'scripts/image/capture_and_evaluate_light.py'], check=True)
        # Load the evaluated ISO and shutter speed values
        light_level, iso, shutter_speed = load_values_from_file()

    log_message(logger, f"Light level: {light_level}, ISO: {iso}, Shutter speed: {shutter_speed}")

    # Determine if it's daylight
    daylight = iso == "auto" and shutter_speed == "auto"

    # Capture the image with the retrieved settings
    capture_image(config, iso, shutter_speed, daylight, logger)

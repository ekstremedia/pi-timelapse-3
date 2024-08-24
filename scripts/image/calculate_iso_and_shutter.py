import os
import yaml

# Configuration parameters
DAYLIGHT_THRESHOLD = 13  # Light level threshold for daylight mode (auto settings)
NIGHT_THRESHOLD = 1      # Light level below which to use maximum ISO and slowest shutter speed
SMOOTHING_START = 70       # Light level at which to start smoothing the transition to daylight settings

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

def calculate_iso_and_shutter(light_level):
    """
    Calculate the ISO and shutter speed based on the light level.

    Parameters:
        light_level (float): The measured light level.

    Returns:
        tuple: (iso_value, shutter_value, daylight)
            iso_value (int or str): Calculated ISO value or "auto" for daylight mode.
            shutter_value (int or str): Calculated shutter speed in microseconds or "auto" for daylight mode.
            daylight (bool): True if the light level is considered daylight, otherwise False.
    """
    # Automatically load the config.yaml from ../../config.yaml
    config_path = os.path.join(os.path.dirname(__file__), '../../config.yaml')
    config = load_config(config_path)

    if light_level >= DAYLIGHT_THRESHOLD:
        # Daylight mode, use auto settings
        return "auto", "auto", True

    elif light_level < NIGHT_THRESHOLD:
        # Night mode, use maximum ISO and slowest shutter speed
        return config['camera_settings']['iso_night'], config['camera_settings']['shutter_speed_night'], False

    # Gradual transition zone (NIGHT_THRESHOLD <= light_level < DAYLIGHT_THRESHOLD)
    iso_range = config['camera_settings']['iso_night'] - config['camera_settings']['iso_day']
    shutter_range = config['camera_settings']['shutter_speed_night'] - config['camera_settings']['shutter_speed_day']

    # Calculate linear position between night and day based on light level
    interpolation_factor = (light_level - NIGHT_THRESHOLD) / (DAYLIGHT_THRESHOLD - NIGHT_THRESHOLD)
    
    iso_value = config['camera_settings']['iso_day'] + (iso_range * (1 - interpolation_factor))
    shutter_value = config['camera_settings']['shutter_speed_day'] + (shutter_range * (1 - interpolation_factor))

    # Clamp values to avoid exceeding limits
    iso_value = int(max(config['camera_settings']['iso_day'], min(iso_value, config['camera_settings']['iso_night'])))
    shutter_value = int(max(config['camera_settings']['shutter_speed_day'], min(shutter_value, config['camera_settings']['shutter_speed_night'])))

    # Smooth the shutter speed transition as it approaches daylight (between SMOOTHING_START and DAYLIGHT_THRESHOLD light level)
    if light_level > SMOOTHING_START:
        transition_range = DAYLIGHT_THRESHOLD - SMOOTHING_START
        relative_light_level = (light_level - SMOOTHING_START) / transition_range
        shutter_value = int((1 - relative_light_level) * shutter_value + relative_light_level * config['camera_settings']['shutter_speed_day'])

    return iso_value, shutter_value, False

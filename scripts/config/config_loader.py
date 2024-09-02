import yaml
import json
import os

def load_config(config_path: str) -> dict:
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return {}

def load_values_from_file(file_path: str = 'temp/last_measurement.json') -> tuple:
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data["light_level"], data["iso"], data["shutter_speed"]
        except Exception as e:
            print(f"Error loading values from file: {e}")
            return None, None, None
    else:
        print(f"No previous measurement found at {file_path}")
        return None, None, None

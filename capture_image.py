import os
import subprocess
from datetime import datetime
import time
from picamera2 import Picamera2
from scripts.log.logging import setup_logger, log_message, setup_logging_directory
from scripts.image.calculate_iso_and_shutter import calculate_iso_and_shutter
from scripts.image.add_image_overlay import overlay_image_with_text
from scripts.config.config_loader import load_config, load_values_from_file
from scripts.image.configure_camera import configure_camera  # Import the configure_camera function
from scripts.image.set_hdr_status import get_current_hdr_state  # Import function to get HDR state

def capture_image(config, iso, shutter_speed, daylight, logger=None):
    try:
        picam2 = Picamera2()
        
        picam2.options["quality"] = config['camera_settings']['image_quality']
        picam2.options["compress_level"] = config['camera_settings']['compress_level']

        camera_config = configure_camera(picam2, config, daylight, iso, shutter_speed, logger)
        picam2.configure(camera_config)  # type: ignore

        # Start the camera and capture the image
        time.sleep(2)  # Allow camera to adjust
        picam2.start()

        now = datetime.now()
        dir_name = os.path.join(config['image_output']['root_folder'], now.strftime(config['image_output']['folder_structure']))
        os.makedirs(dir_name, exist_ok=True)
        file_name = os.path.join(dir_name, f"{config['image_output']['filename_prefix']}{now.strftime('%Y_%m_%d_%H_%M_%S')}.{config['image_output']['image_extension']}")

        picam2.capture_file(file_name)
        picam2.stop()

        # Get the HDR state
        hdr_state = get_current_hdr_state()

        # Log the capture
        log_entry = f"Captured image {file_name} with settings: ISO={iso}, Shutter={shutter_speed}, Quality={picam2.options['quality']}, Compression={picam2.options['compress_level']}, Daylight={daylight}, HDR={hdr_state}, Config={camera_config['controls']}"
        print(log_entry)
        if logger:
            log_message(logger, log_entry)

        # Apply overlay and text to the captured image
        try:
            overlay_data = {
                "ISO": iso,
                "Shutter": shutter_speed,
                "Quality": picam2.options['quality'],
                "Compression": picam2.options['compress_level'],
                "Daylight": daylight,
                "HDR": hdr_state,  # Include HDR state
                "Config": camera_config['controls']
            }
            overlay_image_with_text(file_name, output_image_path=file_name, quality=picam2.options['quality'], overlay_data=overlay_data)
        except Exception as e:
            print(f"Error applying overlay: {e}")
            if logger:
                log_message(logger, f"Error applying overlay: {e}")

        # Create or update symlink to the latest image
        symlink_path = config['image_output']['status_file']
        try:
            if os.path.islink(symlink_path) or os.path.exists(symlink_path):
                os.remove(symlink_path)
            os.symlink(file_name, symlink_path)

            if logger:
                log_message(logger, f"Symlink updated: {symlink_path} -> {file_name}")
        except Exception as e:
            print(f"Error updating symlink: {e}")
            if logger:
                log_message(logger, f"Error updating symlink: {e}")

        print(f"Image captured and saved to {file_name}")

    except Exception as e:
        print(f"Error during image capture: {e}")
        if logger:
            log_message(logger, f"Error during image capture: {e}")

if __name__ == "__main__":
    try:
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
            iso, shutter_speed, _ = calculate_iso_and_shutter(light_level, config) # type: ignore
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

    except Exception as e:
        print(f"Fatal error in main execution: {e}")
        if logger:
            log_message(logger, f"Fatal error in main execution: {e}")
 
Project Overview
This project is designed to automate the process of capturing images with a Raspberry Pi camera, adjusting camera settings based on ambient light conditions, and saving the images in an organized directory structure. The system adjusts camera settings dynamically, switching between daytime and nighttime configurations based on light measurements, ensuring optimal image quality throughout the day.

Scripts Overview
1. config.yaml
Purpose: The central configuration file that stores all the settings for the camera and logging.

Key Sections:

camera_settings: Configuration for the camera, including image size, focus mode, white balance, and more.
image_output: Specifies the directory structure and filename prefix for saving images.
logging: Controls whether logging is enabled for each script.
2. capture_image.py
Purpose: The main script that runs every minute to capture an image based on the current light conditions.

Workflow:

Runs capture_and_evaluate_light.py to capture a low-resolution image and evaluate the light level.
Retrieves the ISO and shutter speed settings based on the light level.
Configures the camera with appropriate settings (daytime or nighttime).
Captures and saves the image in the directory structure defined in config.yaml.
Logs the capture details if logging is enabled.
3. scripts/image/capture_light_valuation_image.py
Purpose: Captures a low-resolution image to evaluate the current light conditions.

Workflow:

Configures the camera using a low-resolution setting for quick image capture.
Saves the image to temp/light_valuation.jpg.
This script is used as a helper by capture_and_evaluate_light.py.
4. scripts/image/capture_and_evaluate_light.py
Purpose: Combines the functionality of capturing an image for light evaluation and determining the ISO and shutter speed settings.

Workflow:

Runs capture_light_valuation_image.py to capture the image.
Analyzes the image to determine the current light level.
Calculates the appropriate ISO and shutter speed settings based on the light level using calculate_iso_and_shutter.py.
Saves the calculated values to temp/last_measurement.json for later use by capture_image.py.
5. scripts/image/calculate_iso_and_shutter.py
Purpose: A utility module that calculates the appropriate ISO and shutter speed settings based on the light level.

Functionality:

Takes in the light level and the configuration settings from config.yaml.
Uses a smooth interpolation to determine ISO and shutter speed values within a range between day and night settings.
Returns the calculated ISO, shutter speed, and whether it’s daylight.
6. scripts/image/get_brightness_of_images.py
Purpose: Analyzes a directory of images to calculate the light levels for each and determine the appropriate camera settings.

Workflow:

Iterates through all images in a specified directory.
Calculates the light level for each image.
Logs the light level, ISO, shutter speed, and whether it’s daylight or not.
7. scripts/log/logging.py
Purpose: Provides a common logging utility for all scripts.

Functionality:

Sets up logging directories and files based on configuration.
Provides utility functions to log messages with timestamps.
Ensures that all logs are written to the appropriate log file if logging is enabled in config.yaml.
Directory Structure
/scripts/image/: Contains all image-related scripts.
/scripts/log/: Contains the logging utility script.
/temp/: Stores temporary files like light_valuation.jpg and last_measurement.json.
/logs/: Stores log files for all the scripts if logging is enabled.
/var/www/html/images/: Directory where captured images are stored, structured by date (e.g., /2024/08/02/).
How It Works
Automatic Image Capture: The capture_image.py script runs every minute. It starts by evaluating the light conditions using capture_and_evaluate_light.py. Based on this evaluation, it configures the camera and captures a high-resolution image, saving it with a timestamped filename.

Dynamic Camera Settings: The ISO and shutter speed are dynamically adjusted based on light levels, ensuring that images are captured with optimal exposure, whether it’s day or night.

Logging: If enabled, all actions and camera settings used during the image capture process are logged to a file, allowing for easy troubleshooting and analysis.

This overview should provide a clear understanding of each script's role in the system and how they interact to achieve automated image capturing and processing.

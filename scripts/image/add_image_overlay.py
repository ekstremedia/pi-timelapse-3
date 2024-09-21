# scripts/image/add_image_overlay.py

import json
from PIL import Image, ImageDraw, ImageFont
import os
import yaml
from datetime import datetime
import locale

# Set the locale to Norwegian
locale.setlocale(locale.LC_TIME, "nb_NO.UTF-8")

# Default configuration
OVERLAY_IMAGE_PATH = os.path.join(os.path.dirname(__file__), '../../overlay/overlay.png')
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 50
TEXT_COLOR = (255, 255, 255)  # White text, no alpha channel for JPEG
TIME_FONT_SIZE = 70  # Font size for the time
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../config.yaml')
QUALITY = 70
LAST_MEASUREMENT_PATH = os.path.join(os.path.dirname(__file__), '../../temp/last_measurement.json')

def load_light_level(last_measurement_path=LAST_MEASUREMENT_PATH):
    """
    Loads the light level from the last_measurement.json file.

    Parameters:
        last_measurement_path (str): Path to the last_measurement.json file.

    Returns:
        float: The light level rounded to one decimal place.
    """
    if os.path.exists(last_measurement_path):
        with open(last_measurement_path, 'r') as file:
            data = json.load(file)
        return round(data.get("light_level", 0), 1)
    else:
        return None

def load_camera_name(config_path=CONFIG_PATH):
    """
    Loads the camera name from the YAML configuration file.

    Parameters:
        config_path (str): Path to the config.yaml file.

    Returns:
        str: The camera name.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config.get('camera_settings', {}).get('name', "Camera Name")

def overlay_image_with_text(input_image_path, output_image_path=None, text=None, quality=QUALITY, overlay_data=None, metadata=None, evlux=None):
    """
    Overlays an image with an overlay image, adds the camera name, and the full date in Norwegian.

    Parameters:
        input_image_path (str): Path to the base image.
        output_image_path (str, optional): Path to save the output image. If None, the input image will be overwritten.
        text (str): Camera name to add to the image.
        quality (int): Quality of the output image (applicable for JPEG format).
        overlay_data (dict): Additional data to be displayed on the image.
    """
    # Load camera name if text is not provided
    if text is None:
        text = load_camera_name()

    # Load the base image
    base_image = Image.open(input_image_path).convert("RGBA")

    # Load the overlay image
    overlay_image = Image.open(OVERLAY_IMAGE_PATH).convert("RGBA")

    # Create a transparent layer the same size as the base image
    transparent_layer = Image.new("RGBA", base_image.size, (0, 0, 0, 0))

    # Paste the overlay onto the transparent layer
    transparent_layer.paste(overlay_image, (0, 0))

    # Composite the base image with the transparent layer containing the overlay
    combined = Image.alpha_composite(base_image, transparent_layer)

    # Add camera name and date text on top of the overlay
    draw = ImageDraw.Draw(combined)
    camerafont = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    datefont = ImageFont.truetype(FONT_PATH, 40)

    # Center the camera name
    text_bbox = draw.textbbox((0, 0), text, font=camerafont)
    text_position = ((base_image.width - text_bbox[2]) // 2, 10)  # 10 pixels from the top edge
    draw.text(text_position, text, font=camerafont, fill=TEXT_COLOR)

    # Add the full date in Norwegian format just below the camera name
    full_date = datetime.now().strftime("%A, %d. %B %Y %H:%M")
    date_bbox = draw.textbbox((0, 0), full_date, font=datefont)
    date_position = ((base_image.width - date_bbox[2]) // 2, text_position[1] + text_bbox[3] + 10)  # 10 pixels below the camera name
    draw.text(date_position, full_date, font=datefont, fill=TEXT_COLOR)

    if overlay_data:
        light_level = load_light_level()
        overlay_font = ImageFont.truetype(FONT_PATH, 30)
        overlay_text = (
            f"ISO: {overlay_data.get('ISO', 'N/A')}, "
            f"Shutter: {overlay_data.get('Shutter', 'N/A')}, "
            f"Light: {light_level}, "
            f"Day: {overlay_data.get('Daylight', 'N/A')}, "
            f"HDR: {'On' if overlay_data.get('HDR') else 'Off'}"  # Include HDR state
        )
        if metadata is not None:
            
            overlay_text_right = ""
            if evlux is not None:
                overlay_text_right += (
                    f"Evlux: {evlux}, "
                )
            overlay_text_right += (
                f"Lux: {metadata['Lux']}, "
                f"Exposuretime: {metadata['ExposureTime']}, "
                f"AGain: {metadata['AnalogueGain']}, "
                f"DGain: {metadata['DigitalGain']}"
            )
            overlay_text_right_line_2 = (
                f"Exposuretime: {metadata['ExposureTime']}, "
                f"LensPosition: {metadata['LensPosition']}, "
                f"SensorTemp: {metadata['SensorTemperature']}"
            )
            draw.text((2450, 25), overlay_text_right, font=overlay_font, fill=TEXT_COLOR)
            draw.text((2450, 80), overlay_text_right_line_2, font=overlay_font, fill=TEXT_COLOR)

        # Draw the text
        draw.text((20, 85), overlay_text, font=overlay_font, fill=TEXT_COLOR)
        
    # Convert the final image to RGB mode (JPEG doesn't support alpha channel)
    final_image = combined.convert("RGB")

    # Save the result as a JPEG with the specified quality
    if output_image_path is None:
        output_image_path = input_image_path

    final_image.save(output_image_path, "JPEG", quality=quality, optimize=True)
    # print(f"Overlay added and saved to {output_image_path}")


def test_overlay_image(input_image_path, output_image_path):
    """
    Test function to apply overlay and save to a specified output image.

    Parameters:
        input_image_path (str): Path to the base image.
        output_image_path (str): Path to save the output image.
    """
    overlay_image_with_text(input_image_path, output_image_path)

# Example usage in a script
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        # Test mode: python add_image_overlay.py input_image output_image
        test_overlay_image(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        # Normal mode: overlay image and save to the same file
        overlay_image_with_text(sys.argv[1])
    else:
        print("Usage:")
        print("  python add_image_overlay.py input_image output_image")
        print("  or")
        print("  python add_image_overlay.py input_image")

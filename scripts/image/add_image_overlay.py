from PIL import Image, ImageDraw, ImageFont
import os

# Default configuration
OVERLAY_IMAGE_PATH = os.path.join(os.path.dirname(__file__), '../../overlay/overlay.png')
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 50
TEXT_COLOR = (255, 255, 255)  # White text, no alpha channel for JPEG
DEFAULT_TEXT = "Test"
TEXT_POSITION = (20, 70)  # Position where the text will be added over the overlay

def overlay_image_with_text(input_image_path, output_image_path=None, text=DEFAULT_TEXT, text_position=TEXT_POSITION, quality=85):
    """
    Overlays an image with an overlay image and adds text on top.

    Parameters:
        input_image_path (str): Path to the base image.
        output_image_path (str, optional): Path to save the output image. If None, the input image will be overwritten.
        text (str): Text to add to the image.
        text_position (tuple): Position where the text should be placed.
        quality (int): Quality of the output image (applicable for JPEG format).
    """
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

    # Add text on top of the overlay
    draw = ImageDraw.Draw(combined)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw.text(text_position, text, font=font, fill=TEXT_COLOR)

    # Convert the final image to RGB mode (JPEG doesn't support alpha channel)
    final_image = combined.convert("RGB")

    # Save the result as a JPEG
    if output_image_path is None:
        output_image_path = input_image_path

    final_image.save(output_image_path, "JPEG", quality=quality)
    print(f"Image saved to {output_image_path}")

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

import os
from PIL import Image

# Directory containing the images
image_dir = "/var/www/html/lys-spjutvika/"

# List all image files in the directory
image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]

# Crop each image
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    image = Image.open(image_path)
    
    # Crop the top 100 pixels (adjust this value as needed)
    cropped_image = image.crop((0, 120, image.width, image.height))
    
    # Save the cropped image, replacing the original
    cropped_image.save(image_path)

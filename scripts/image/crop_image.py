import os
from PIL import Image

def crop_images_in_directory(directory):
    """
    Crops the top 120 pixels from all images in the specified directory.
    
    Parameters:
        directory (str): Path to the directory containing the images.
    """
    # List all image files in the directory
    image_files = [f for f in os.listdir(directory) if f.endswith('.jpg')]

    # Crop each image
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        image = Image.open(image_path)
        
        # Crop the top 120 pixels (adjust this value as needed)
        cropped_image = image.crop((0, 120, image.width, image.height))
        
        # Save the cropped image, replacing the original
        cropped_image.save(image_path)
        print(f"Cropped and saved {image_file}")

if __name__ == "__main__":
    # Directory containing the images
    image_dir = "/var/www/html/lys-spjutvika/"
    
    # Confirmation prompt
    response = input(f"Are you sure you want to crop the images in the directory '{image_dir}'? This action cannot be undone. (Yes/No): ")
    
    if response.lower() in ['yes', 'y']:
        crop_images_in_directory(image_dir)
        print("Cropping completed.")
    else:
        print("Operation cancelled.")

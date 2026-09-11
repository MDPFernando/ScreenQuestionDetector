from PIL import Image
import os

img_path = r"C:\Users\dinet\.gemini\antigravity-ide\brain\fb4676a8-7896-4e7e-b731-362aba1651e8\app_icon_design_1789100601254.jpg"

if os.path.exists(img_path):
    img = Image.open(img_path)
    
    # The generated image has the icon in the center. We crop the central 600x600 portion.
    width, height = img.size
    crop_size = 600
    left = (width - crop_size) / 2
    top = (height - crop_size) / 2
    right = (width + crop_size) / 2
    bottom = (height + crop_size) / 2
    
    cropped_img = img.crop((left, top, right, bottom))
    
    # Save as multi-size ICO file for Windows
    icon_sizes = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
    cropped_img.save("icon.ico", format="ICO", sizes=icon_sizes)
    print("Successfully created icon.ico")
else:
    print("Error: Generated image not found.")

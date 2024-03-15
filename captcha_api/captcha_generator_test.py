from io import BytesIO
from PIL import Image
import os
from captcha_generator import CaptchaGenerator

# Ensure you have the CaptchaGenerator class defined as previously discussed

def generate_and_save_captchas(num_captchas=100, save_dir="captchas"):
    # Create a directory to save the captcha images if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    generator = CaptchaGenerator()

    for i in range(num_captchas):
        img_byte_array, text = generator.generate_captcha()
        # Convert the byte array to an image
        img = Image.open(BytesIO(img_byte_array.getvalue()))
        # Construct the filename using the captcha text (or a sequence number if you prefer)
        filename = f"{text}_{i}.jpg"
        save_path = os.path.join(save_dir, filename)
        # Save the image
        img.save(save_path, format="JPEG")
        print(f"Saved {save_path}")

# Call the function to generate and save 100 captcha images
generate_and_save_captchas()
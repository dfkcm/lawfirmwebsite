import os
import secrets
import uuid
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename
import random
import string

def save_image(file, folder='uploads'):
    """Save an image to the specified folder and return the filename"""
    if not file:
        return None
    
    # Create a secure filename
    filename = secure_filename(file.filename)
    # Generate a unique filename to avoid overwriting
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(filename)
    new_filename = random_hex + file_extension
    
    # Create the upload path if it doesn't exist
    upload_path = os.path.join(current_app.root_path, 'static', folder)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    
    # Save the file
    file_path = os.path.join(upload_path, new_filename)
    
    # Resize and save image
    image = Image.open(file)
    # Set a max size for the image if needed
    image.thumbnail((1200, 1200))
    image.save(file_path)
    
    return new_filename

def generate_captcha_code(length=6):
    """Generate a random captcha code"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def delete_image(filename, folder='uploads'):
    """Delete an image from the specified folder"""
    if not filename:
        return False
    
    file_path = os.path.join(current_app.root_path, 'static', folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

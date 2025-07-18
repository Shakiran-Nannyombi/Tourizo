import os
import secrets
import uuid
from PIL import Image
from flask import current_app

def save_picture(form_picture, folder):
    if not form_picture:
        return None
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads', folder)
    os.makedirs(upload_path, exist_ok=True)
    picture_path = os.path.join(upload_path, picture_fn)
    img = Image.open(form_picture)
    img.thumbnail((800, 600))
    img.save(picture_path)
    return picture_fn

def generate_booking_reference():
    return 'TB' + str(uuid.uuid4()).replace('-', '')[:8].upper() 
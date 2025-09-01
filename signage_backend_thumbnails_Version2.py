import os
from .settings import load_config
from PIL import Image
import subprocess

def generate_thumbnail(asset):
    config = load_config()
    thumbs_dir = config['thumb_dir']
    os.makedirs(thumbs_dir, exist_ok=True)
    thumb_path = os.path.join(thumbs_dir, f"{asset.id}.jpg")
    if asset.type == "image":
        im = Image.open(asset.path)
        im.thumbnail((320, 180))
        im.save(thumb_path, "JPEG")
    elif asset.type == "video":
        # Extract 1st frame with ffmpeg
        subprocess.run([
            "ffmpeg", "-y", "-i", asset.path, "-ss", "00:00:01.000",
            "-vframes", "1", thumb_path
        ])
    asset.thumb_path = thumb_path
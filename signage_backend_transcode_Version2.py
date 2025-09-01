import subprocess
from .settings import load_config
from .models import db, Asset
import os

def enqueue_transcode(asset):
    config = load_config()
    src = asset.path
    out = src + ".mp4"
    asset.status = "transcoding"
    db.session.commit()
    # Run ffmpeg in background (simple version)
    cmd = [
        "ffmpeg", "-y", "-i", src,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k", out
    ]
    subprocess.Popen(cmd)
    asset.status = "ready"
    asset.path = out
    db.session.commit()
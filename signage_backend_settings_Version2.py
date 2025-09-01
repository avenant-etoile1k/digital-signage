import yaml
import os

DEFAULTS = {
    "db_path": "/home/signage/digital-signage/signage/data/signage.db",
    "media_dir": "/home/signage/digital-signage/media",
    "thumb_dir": "/home/signage/digital-signage/thumbs",
    "log_dir": "/home/signage/digital-signage/logs",
    "default_orientation": "landscape",
    "default_volume": 70,
    "default_resolution": "1920x1080",
    "web_timeout_sec": 12,
    "max_upload_size_mb": 250,
    "whitelist_exts": [".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mkv", ".mp3", ".aac", ".wav"],
    "lang": "fr",
    "quota_mb": 12000,
    "log_level": "INFO",
    "watch_folder": "/home/signage/digital-signage/watch"
}

def load_config():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/config.yaml"))
    config = DEFAULTS.copy()
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            user_conf = yaml.safe_load(f)
            if user_conf:
                config.update(user_conf)
    return config
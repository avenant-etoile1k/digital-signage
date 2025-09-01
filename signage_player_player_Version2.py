#!/usr/bin/env python3
import os
import time
import yaml
import json
import subprocess
from python_mpv_jsonipc import MPV
import requests

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/config.yaml"))

def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

def get_active_playlist():
    try:
        resp = requests.get("http://localhost:8080/active-playlist")
        return resp.json()
    except:
        return []

def show_fallback(ip):
    # Use mpv to show black screen with overlay text
    subprocess.run([
        "mpv", "--fs", "--no-osc", "--hwdec=auto",
        "--image-display-duration=3600",
        "--sub-font-size=48",
        "--sub-text='Digital Signage – IP : {} – Connectez-vous à http://{}:8080'".format(ip, ip),
        "--", "/dev/null"
    ])

def apply_orientation(orientation):
    output = "HDMI-1"
    rotate = "left" if orientation == "portrait" else "normal"
    subprocess.run(["xrandr", "--output", output, "--rotate", rotate])

def get_local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def main():
    config = load_config()
    apply_orientation(config.get("default_orientation", "landscape"))
    mpv = MPV(input_default_bindings=True, input_vo_keyboard=True, wid=None)
    while True:
        playlist = get_active_playlist()
        if not playlist:
            show_fallback(get_local_ip())
            time.sleep(10)
            continue
        for item in playlist['items']:
            typ = item['type']
            path = item['path']
            duration = item.get('duration_sec', 10)
            volume = item.get('volume', config.get('default_volume', 70))
            if typ == "image":
                mpv.play(path)
                mpv.set_property("volume", volume)
                time.sleep(duration)
                mpv.stop()
            elif typ == "video":
                mpv.play(path)
                mpv.set_property("volume", volume)
                # Wait for playback or max duration
                t0 = time.time()
                while mpv.playback_time < item.get('max_duration_sec', 9999):
                    if not mpv.core_idle:
                        time.sleep(1)
                        if time.time() - t0 > duration:
                            mpv.stop()
                            break
                mpv.stop()
            elif typ == "audio":
                mpv.play(path)
                mpv.set_property("volume", volume)
                # Display black background or static image
                time.sleep(duration)
                mpv.stop()
            elif typ == "web":
                url = item['url']
                duration = item.get("duration_sec", 10)
                subprocess.Popen([
                    "chromium-browser",
                    "--kiosk", "--incognito", "--app=%s" % url
                ])
                time.sleep(duration)
                subprocess.run(["pkill", "-f", "chromium-browser"])
            else:
                continue
            # Fade to black
            time.sleep(0.3)
        time.sleep(1)

if __name__ == "__main__":
    main()
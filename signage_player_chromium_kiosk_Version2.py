import subprocess
import time

def run_chromium_kiosk(url, duration_sec):
    proc = subprocess.Popen([
        "chromium-browser", "--kiosk", "--incognito", "--app=%s" % url
    ])
    time.sleep(duration_sec)
    proc.terminate()
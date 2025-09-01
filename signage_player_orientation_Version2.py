import subprocess

def apply_orientation(orientation):
    output = "HDMI-1"
    rotate = "left" if orientation == "portrait" else "normal"
    subprocess.run(["xrandr", "--output", output, "--rotate", rotate])
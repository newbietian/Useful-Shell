"""
This is a way to save the startup time when running img2py on lots of
files...
"""
import base64
import sys

images = [
    {"name": "logo", "path": "android-log-analysis-tool-background-title-v1.jpg"},
    {"name": "icon", "path": "icon.ico"},
    {"name": "action_new", "path": "action_new.png"},
]

if __name__ == "__main__":
    target = open("html_images.py", "a")
    for file_dict in images:
        name = file_dict["name"]
        path = file_dict["path"]
        with open(path, "rb") as f:
            base64_data = base64.b64encode(f.read())
            target.write('%s = "%s"' % (name, base64_data))
            target.write("\n")
            f.close()
    target.close()


"""
This is a way to save the startup time when running img2py on lots of
files...
"""

import sys
from wx.tools import img2py


command_lines = [
    "   -F -n clean_history clean_history.png    images.py",
    "-a -F -n error error.png                    images.py",
    "-a -F -n info info.png                      images.py",
    "-a -F -n new new.png                        images.py",
    "-a -F -n splash splash.png                  images.py",
    "-a -F -n success success.png                images.py"
    ]

if __name__ == "__main__":
    for line in command_lines:
        args = line.split()
        img2py.main(args)


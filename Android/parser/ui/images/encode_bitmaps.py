
"""
This is a way to save the startup time when running img2py on lots of
files...
"""

import sys
from wx.tools import img2py


command_lines = [
    "   -F -n action_clean_history        action_clean_history.png              images.py",
    "-a -F -n action_new                  action_new.png                        images.py",
    "-a -F -n app_splash                  app_splash.png                        images.py",
    "-a -F -n web_service_error           web_service_error.png                 images.py",
    "-a -F -n web_service_info            web_service_info.png                  images.py",
    "-a -F -n web_service_success         web_service_success.png               images.py",
    "-a -F -n task_done                   task_done.png                         images.py",
    "-a -F -n task_process                task_process.png                      images.py",
    "-a -F -n task_paused                 task_paused.png                        images.py",
    "-a -F -n task_waiting                task_waiting.png                      images.py",
    "-a -F -n task_generating             task_generating.png                   images.py"
    ]

if __name__ == "__main__":
    for line in command_lines:
        args = line.split()
        img2py.main(args)


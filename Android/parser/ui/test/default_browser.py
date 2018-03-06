#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import sys
import webbrowser

sys.path.append("libs")

url = 'https://www.baidu.com'
webbrowser.open(url)
print webbrowser.get()
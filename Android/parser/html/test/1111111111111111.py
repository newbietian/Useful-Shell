# -*- coding=utf-8 -*-

import HTML
import tool.tools as tool
import os
import html_images

html_file = 'test111.html'
f = open(html_file, 'w')

# === TABLES ===================================================================

title = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
         "http://www.w3.org/TR/html4/loose.dtd">
 <html>
 <head>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
     <meta name="viewport" content="width=device-width, initial-scale=1">
     <title id="head_title"></title>
     <style type="text/css"></style>
     <link rel='icon' href='data:image/x-icon;base64,{icon}' type=‘image/x-ico’/>
     <link rel="stylesheet" type="text/css" href="{style}"/>
 </head>

 <body>

 <script src="{webserver}" type="text/javascript"></script>

 <div>
     <table align="center" class="title">
         <tr>
             <td align="center">
                 <img src="data:image/jpg;base64,{logo}" complete="complete">
             </td>
         </tr>
         <tr>
             <td align="center">
                 <h4><font color="#FF0000" size="4">{error_type}</font> in <a id="connect" href="">{log_path}</a>, 生成于 {create_time}</h4>
             </td>
         </tr>
     </table>
 </div>"""

error_type = "Fatal Exception"
log_path = "/home/qinsw/downloads/android/log"

f.write(title.format(
    icon=html_images.icon,
    style="fatal_exception.css",
    webserver="../js/websocket.js",
    logo=html_images.logo,
    error_type=error_type,
    log_path=log_path,
    create_time=tool.get_format_time()
) + '\n\n')

# fatal exception
table_data = [
    [HTML.link('java.lang.NullPointerException: Attempt to invoke virtual method', 'https://www.baidu.com'), 10,
     tool.get_format_time()],
    [HTML.link('java.lang.ArrayIndexOutOfBoundsException: length=0; index=-1', 'https://www.baidu.com'), 22,
     tool.get_format_time()],
    [HTML.link('java.lang.SecurityException: Permission Denial', 'https://www.baidu.com'), 33,
     tool.get_format_time()],
    [HTML.link('java.lang.SecurityException: Permission Denial', 'https://www.baidu.com'), 33,
     tool.get_format_time()],
    [HTML.link('java.lang.SecurityException: Permission Denial', 'https://www.baidu.com'), 33,
     tool.get_format_time()],
    [HTML.link('java.lang.SecurityException: Permission Denial', 'https://www.baidu.com'), 33,
     tool.get_format_time()],
    [HTML.link('java.lang.SecurityException: Permission Denial', 'https://www.baidu.com'), 33,
     tool.get_format_time()],
    [HTML.link('java.lang.SecurityException: Permission Denial', 'https://www.baidu.com'), 33,
     tool.get_format_time()],
    [HTML.link('java.lang.SecurityException: Permission Denial', 'https://www.baidu.com'), 33,
     tool.get_format_time()],
    [HTML.link('java.lang.SecurityException: Permission Denial', 'https://www.baidu.com'), 33,
     tool.get_format_time()],
    [HTML.link('java.lang.SecurityException: Permission Denial', 'https://www.baidu.com'), 33,
     tool.get_format_time()],
    [HTML.link('java.lang.SecurityException: Permission Denial', 'https://www.baidu.com'), 33,
     tool.get_format_time()],
]

htmlcode = HTML.table(table_data,
                      header_row=['Exception', 'Count', 'First Occurred time'],
                      border='1',
                      style='fatal_exception.css',
                      attribs={"class": "summary"},
                      col_width=['', '10%', '20%'],
                      col_align=['left', 'center', 'center'],
                      col_styles=['font-size: large', '', ''])
f.write(htmlcode + '<p>\n')


htmlcode = HTML.table(table_data,
                      header_row=['Exception', 'Count', 'First Occurred time'],
                      border='1',
                      style='fatal_exception.css',
                      attribs={"class": "summary"},
                      col_width=['', '10%', '20%'],
                      col_align=['left', 'center', 'center'],
                      col_styles=['font-size: large', '', ''])
f.write(htmlcode + '<p>\n')
f.close()

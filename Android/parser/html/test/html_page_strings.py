# -*- coding=utf-8 -*-

exception_page_html_head = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
         "http://www.w3.org/TR/html4/loose.dtd">
 <html>
 <head>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
     <meta name="viewport" content="width=device-width, initial-scale=1">
     <title id="head_title">{page_title}</title>
     <style type="text/css"></style>
     <link rel='icon' href='data:image/x-icon;base64,{page_icon}' type=‘image/x-ico’/>
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
                 <h4><font color="#FF0000" size="4">{error_type}s</font> in <a id="connect" href="">{log_path}</a>, 生成于 {create_time}</h4>
             </td>
         </tr>
     </table>
 </div>"""
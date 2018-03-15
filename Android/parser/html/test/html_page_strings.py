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

exception_page_css = """
/* Copyright (C) 2015 The Android Open Source Project

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

body {
    font-family:arial,sans-serif;
    color:#000;
    font-size:13px;
    color:#333;
    padding:10px;
    margin: 10px;
}

/* Report logo and device name */
table.title {
    padding:5px;
    border-width: 0px;
    margin-left:auto;
    margin-right:auto;
    vertical-align:middle;
}

logo {
    background: rgb(212, 233, 169);
    margin-left:1000px;
}

table.summary {
    background: rgb(212, 233, 169);
    border-collapse:collapse;
    margin-left:auto;
    margin-right:auto;
}

table.summary th {
    background: #A5C639;
    border: 1px outset gray;
    padding: 0.5em;
}

table.summary td {
    border: 1px outset #A5C639;
    padding: 0.5em;
}

table.detailTitle {
    background:  rgb(212, 233, 169);
    border-collapse:collapse;
    margin-left:auto;
    margin-right:auto;
}

table.detailTitle th {
    background: #A5C639;
    border: 1px outset gray;
    padding: 0.5em;
}

table.detailTitle td {
    border: 1px outset #gray;
    padding: 0.5em;
}

table.detailContent {
    background:  rgb(212, 233, 169);
    border-collapse:collapse;
    margin-left:auto;
    margin-right:auto;
}

table.detailContent th {
    background: rgb(212, 233, 169);
    border: 1px outset gray;
    padding: 0.5em;
}

table.detailContent td {
    border: 1px outset gray;
    padding: 0.5em;
}

table.detailTitle1 {
    background:  #ffc0a0;
    border-collapse:collapse;
    margin-left:auto;
    margin-right:auto;
}

table.detailTitle1 th {
    background: #ff6020;
    border: 1px outset gray;
    padding: 0.5em;
}

table.detailTitle1 td {
    border: 1px outset #gray;
    padding: 0.5em;
}

table.detailContent1 {
    background:  #ffc0a0;
    border-collapse:collapse;
    margin-left:auto;
    margin-right:auto;
}

table.detailContent1 th {
    background: #ffc0a0;
    border: 1px outset gray;
    padding: 0.5em;
}

table.detailContent1 td {
    border: 1px outset gray;
    padding: 0.5em;
}

table.processdetails {
    background-color: rgb(212, 233, 169);
    border-collapse:collapse;
    border-width:1px;
    border-color: #A5C639;
    margin-left:auto;
    margin-right:auto;
    margin-bottom: 2em;
    vertical-align: top;
    width: 95%;
}

table.processdetails th {
    background-color: #A5C639;
    border-width: 1px;
    border-color: gray;
    border-style: outset;
    height: 2em;
    padding: 0.2em;
}

table.processdetails td {
    border-width: 1px;
    border-color: #A5C639;
    border-style: outset;
    text-align: left;
    vertical-align: top;
    padding: 0.2em;
}

table.processdetails td.Process {
    background-color: white;
    border: 0px;
    font-weight: bold;
}

/* Process details */
td.callstack {
    text-align: left;
}

td.processname {
    border-width: 1px;
    border-color: #A5C639;
    border-style: outset;
    text-align: left;
    vertical-align: top;
    padding:1;
    overflow:hidden;
}

td.PID {
    border-width: 1px;
    border-color: #A5C639;
    border-style: outset;
    text-align: left;
    vertical-align: top;
    padding:1px;
    overflow:hidden;
}

td.adbfile {
    border-width: 1px;
    border-color: #A5C639;
    border-style: outset;
    text-align: left;
    vertical-align: top;
    padding:1px;
    overflow:hidden;
}


div.details {
    white-space: pre-wrap;       /* css-3 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
    overflow:auto;
}

"""
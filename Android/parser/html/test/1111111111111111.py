# -*- coding=utf-8 -*-

import HTML
import tool.tools as tool
import html_images
import html_page_strings

__M_JAVA__ = "Java Crash"
__M_NATIVE__ = "Native Crash"
__M_ANR__ = "ANR"

html_file = 'test111.html'
f = open(html_file, 'w')

# --------------------------------------


title = html_page_strings.exception_page_html_head
style = "fatal_exception.css"
web_server = "../js/websocket.js"
error_type = "Fatal Exception"
log_path = "/home/qinsw/downloads/android/log"
page_title = "%s in %s" % (error_type, log_path)

f.write(title.format(
    page_title=page_title,
    page_icon=html_images.icon,
    style=style,
    webserver=web_server,
    logo=html_images.logo,
    error_type=error_type,
    log_path=log_path,
    create_time=tool.get_format_time()
) + '\n')

# --------------------------------------

data = {}
exceptions_data = data[__M_JAVA__]

# Exception的Summary
exceptions_summary_data = []
for i, r in enumerate(exceptions_data):
    # 单行数据为： 包名+原因， 次数， 第一次时间
    s_row = [HTML.link('%s %s' % (r.name_package, r.reason), '#%d' % i),
             len(r.base_info_set),
             r.base_info_set[0]
             ]
    exceptions_summary_data.append(s_row)

page_summary = HTML.table(exceptions_summary_data,
                          header_row=['Exception', 'Count', 'First Occurred time'],
                          attribs={"class": "summary"},
                          col_width=['', '10%', '20%'],
                          col_align=['left', 'center', 'center'],
                          col_styles=['font-size: large', '', ''])
f.write(page_summary + '<p>\n')

for i in range(60):
    f.write('<br>\n')

data1 = [
    ["com.android.settings",
     "java.lang.NullPointerException: Attempt to invoke virtual method",
     "java.lang.RuntimeException: Buffer not large enough for pixels" + "<br/>" + \
     "at android.graphics.Bitmap.copyPixelsFromBuffer(Bitmap.java:593)" + "<br/>" + \
     "at com.android.browser.Tab.updateCaptureFromBlob(Tab.java:2070)" + "<br/>" + \
     "at com.android.browser.DataController$DataControllerHandler.doLoadThumbnail(DataController.java:233)"
     ],
]

page_content = HTML.table(data1,
                          header_row=['Package', 'Reason', 'StackTrace'],
                          width=1180,
                          attribs={"class": "detailTitle", "id": "1"},
                          col_width=['', '30%', '60%'],
                          col_align=['center', 'center', 'left'],
                          col_styles=['font-size: large', 'font-size: medium', '']
                          )

f.write(page_content + '<p>\n')

data2 = [
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],

]

page_details = HTML.table(data2,
                          header_row=['PID', 'Occurred Time', 'Adb Log'],
                          width=1180,
                          attribs={"class": "detailContent"},
                          col_width=['10%', '30%', '60%'],
                          col_align=['center', 'center', 'center'],
                          col_styles=['font-size: large', '', '']
                          )
f.write(page_details + '<p>\n')

for i in range(60):
    f.write('<br>\n')

data1 = [
    ["com.android.wallpaperpicker",
     "java.lang.NullPointerException: Attempt to invoke virtual method",
     "java.lang.RuntimeException: Buffer not large enough for pixels" + "<br/>" + \
     "at android.graphics.Bitmap.copyPixelsFromBuffer(Bitmap.java:593)" + "<br/>" + \
     "at com.android.browser.Tab.updateCaptureFromBlob(Tab.java:2070)" + "<br/>" + \
     "at com.android.browser.DataController$DataControllerHandler.doLoadThumbnail(DataController.java:233)"
     ],
]

page_content = HTML.table(data1,
                          header_row=['Package', 'Reason', 'StackTrace'],
                          width=1180,
                          attribs={"class": "detailTitle", "id": "2"},
                          col_width=['', '30%', '60%'],
                          col_align=['center', 'center', 'left'],
                          col_styles=['font-size: large', 'font-size: medium', '']
                          )

f.write(page_content + '<p>\n')

data2 = [
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
    [1234, tool.get_format_time(),
     "/data/VM/ShareFolder/11111/trace_analysis/sample_logs/asrlog-2017-11-21-17-17-13/1/android/crash-17-17-13.log(line:2386)"],
]

page_details = HTML.table(data2,
                          header_row=['PID', 'Occurred Time', 'Adb Log'],
                          width=1180,
                          attribs={"class": "detailContent"},
                          col_width=['10%', '30%', '60%'],
                          col_align=['center', 'center', 'center'],
                          col_styles=['font-size: large', '', '']
                          )
f.write(page_details + '<p>\n')

f.close()

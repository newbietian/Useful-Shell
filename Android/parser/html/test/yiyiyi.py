# -*- coding=utf-8 -*-

import HTML
import tool.tools as tool
import html_images
import html_page_strings

__M_JAVA__ = "Java Crash"
__M_NATIVE__ = "Native Crash"
__M_ANR__ = "ANR"


def gen(task, data):
    css_file = '/tmp/fatal_exception.css'
    css = open(css_file, 'w')
    css.write(html_page_strings.exception_page_css)
    css.close()

    html_file = '/tmp/test111.html'
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

    # _data = data
    exceptions_data = data[__M_JAVA__]

    # Exception的Summary数据
    exceptions_summary_data = []
    for i, r in enumerate(exceptions_data):
        # 单行数据为： 包名+原因， 次数， 第一次时间
        s_row = [HTML.link('%s %s' % (r.name_package, r.reason), '#%d' % i),
                 len(r.base_info_set),
                 r.base_info_set[0].occurred_time
                 ]
        exceptions_summary_data.append(s_row)

    page_summary = HTML.table(exceptions_summary_data,
                              header_row=['Exception', 'Count', 'First Occurred time'],
                              attribs={"class": "summary"},
                              col_width=['', '10%', '20%'],
                              col_align=['left', 'center', 'center'],
                              col_styles=['font-size: medium', '', '']
                              )

    f.write(page_summary + '<p>\n')

    for i, r in enumerate(exceptions_data):
        # 留空白
        f.write('<br>\n' * 60)

        # 每个结果的包名，原因和堆栈
        stack_trace = ""
        for st in r.stack_trace:
            stack_trace += (st + "<br/>")
        #print stack_trace
        content_title_data = [
            [  # 包名
                r.name_package,
                # 原因
                r.reason,
                # 堆栈
                str(stack_trace)
            ]
        ]

        page_content_title = HTML.table(content_title_data,
                                        header_row=['Package', 'Reason', 'StackTrace'],
                                        width=1180,
                                        attribs={"class": "detailTitle", "id": "%d" % i},
                                        col_width=['', '30%', '60%'],
                                        col_align=['center', 'center', 'left'],
                                        #col_styles=['font-size: large', 'font-size: medium', '']
                                        )
        f.write(page_content_title + '<p>\n')

        # 对应重复的详细数据： pid， 发生时间，在log中的位置
        base_info_set = []
        for bi in r.base_info_set:
            base_info_set.append([bi.p_t_id,
                                  bi.occurred_time,
                                  "%s(line:%s)" % (bi.location_in_log.log_file_path, bi.location_in_log.found_line)
                                  ])

        page_content_details = HTML.table(base_info_set,
                                          header_row=['PID', 'Occurred Time', 'Adb Log'],
                                          width=1180,
                                          attribs={"class": "detailContent"},
                                          col_width=['10%', '30%', '60%'],
                                          col_align=['center', 'center', 'center'],
                                          col_styles=['font-size: large', '', '']
                                          )
        f.write(page_content_details + '<p>\n')
    f.close()

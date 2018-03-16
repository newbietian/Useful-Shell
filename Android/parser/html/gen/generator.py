# -*- coding=utf-8 -*-

import HTML
import os
import html_page_strings
import html_images
import json
import shutil

import tool.tools as tool

LOG_TAG = "Generator"

__M_JAVA__ = "Java Crash"
__M_NATIVE__ = "Native Crash"
__M_ANR__ = "ANR"


def generate_results(task, data):
    """
    创建所有相关的文件
    :param task: 任务信息，主要是路径
    :param data: 经过解析，最终得到的数据
    """

    # 目录结构：
    # 第一级：
    #       文件：overview.html
    #       目录： exceptions, signals, js
    # 第二级：
    #       exceptions：
    #           exceptions.html, exceptions.css
    #       signals:
    #           signals.html, signals.css
    #       js:
    #           overview_data.js, exporting.js, highcharts.js

    num_exception = len(data[__M_JAVA__])
    num_signal = len(data[__M_NATIVE__])
    num_anr = len(data[__M_ANR__])

    p, f = os.path.split(task.log_path)
    result_path = p + "/%s.alar" % f

    # 创建对应的目录
    try:
        if tool.checkDirExists(result_path):
            shutil.rmtree(result_path)
        os.mkdir(result_path)
    except OSError, e:
        tool.log(LOG_TAG, "create folder { %s } failed, reason: { %s }" % (result_path, e.message))
        return False

    result_links = {}

    # 判断并创建exceptions
    if num_exception > 0:
        exception_link = generate_fatal_exception(result_path, data=data)
        result_links[__M_JAVA__] = exception_link

    # 判断并创建signals
    if num_signal > 0:
        signal_link = generate_fatal_signal(result_path, data=data)
        result_links[__M_NATIVE__] = signal_link

    overview_path = ''
    if len(result_links) > 0:
        # 创建overview
        # .1 创建overview_data.js
        create_overview_data(result_path, data=data, result_links=result_links)
        # .2 创建overview.html
        overview_path = create_overview(result_path)
    return overview_path


def generate_fatal_exception(folder, data):
    """
    创建Fatal Exception的html文件
    :param folder 指定的结果存放目录
    :param data: 存储着fatal exception的数据
    """
    exception_folder = folder + "/exceptions"

    try:
        os.mkdir(exception_folder)
    except OSError, e:
        tool.log(LOG_TAG, "create folder { %s } failed, reason: { %s }" % (exception_folder, e.message))
        return False

    css_file = exception_folder + '/exception.css'
    css = open(css_file, 'w')
    css.write(html_page_strings.exception_page_css)
    css.close()

    html_file = exception_folder + '/exception.html'
    f = open(html_file, 'w')

    # --------------------------------------

    title = html_page_strings.exception_page_html_head
    style = "exception.css"
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
        s_row = [HTML.link('%s - [%s]' % (r.name_package, r.reason), '#%d' % i),
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
        # print stack_trace
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
                                        col_align=['center', 'left', 'left'],
                                        # col_styles=['font-size: large', 'font-size: medium', '']
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
    return html_file


def generate_fatal_signal(task, data):
    return ""


def create_overview_data(folder, data, result_links):
    """
    在js文件夹下创建overview_data.js
    :param folder: 目录
    :param data:
    :return:
    """
    data_folder = folder + "/js"

    try:
        os.mkdir(data_folder)
    except OSError, e:
        tool.log(LOG_TAG, "create folder { %s } failed, reason: { %s }" % (data_folder, e.message))
        return False

    third_party_exporting = open(data_folder + '/exporting.js', 'w')
    print html_page_strings.exporting_js
    third_party_exporting.write(html_page_strings.exporting_js)
    third_party_exporting.close()

    third_party_highcharts = open(data_folder + "/highcharts.js", 'w')
    # print html_page_strings.highcharts_js
    third_party_highcharts.write(html_page_strings.highcharts_js)
    third_party_highcharts.close()

    overview_data = {
        "head_title": "ALAT in %s" % folder,
        "chart_title": tool.get_format_time(),
        "chart_data": [],
    }

    for key in data.keys():
        print key
        if len(data[key]) > 0:
            module_data = {
                "name": key,
                # y代表的是数量
                "y": 0,
                "link": result_links[key]
            }

            y = 0
            for r in data[key]:
                y += len(r.base_info_set)

            module_data["y"] = y
            overview_data["chart_data"].append(module_data)

    # TODO Delete soon for test
    overview_data["chart_data"].append({
                "name": __M_NATIVE__,
                # y代表的是数量
                "y": 100,
                "link": ''
            })

    od = open(data_folder + "/overview_data.js", 'w')
    od.write("var Overview = ")
    od.write(json.dumps(overview_data, indent=2, sort_keys=True))
    od.close()


def create_overview(folder):
    """
    根据主目录路径创建Overview网页文件
    :param folder:
    """
    overview_content = html_page_strings.overview_html.format(
        icon=html_images.icon,
        logo=html_images.logo,
        script=html_page_strings.overview_script
    )

    overview_path = folder + "/" + "overview.html"
    overview = open(overview_path, "w")
    overview.write(overview_content)
    overview.close()
    return overview_path

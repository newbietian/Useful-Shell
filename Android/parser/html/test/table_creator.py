# -*- coding=utf-8 -*-

import HTML
import tool.tools as tool
import os

LOG_TAG = "Generator"
__M_JAVA__ = "Java Crash"
__M_NATIVE__ = "Native Crash"
__M_ANR__ = "ANR"


def generate_result(task, data):
    html_file = 'HTML_tutorial_output.html'
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
        <link rel='icon' href='icon.ico' type=‘image/x-ico’/>
        <link rel="stylesheet" type="text/css" href="fatal_exception.css"/>
    </head>
    
    <body>
    
    <script src="../js/websocket.js" type="text/javascript"></script>
    
    <div>
        <table align="center" class="title">
            <tr>
                <td align="center">
                    <img src="data:image/jpg;base64,{ logo }" complete="complete">
                </td>
            </tr>
            <tr>
                <td align="center">
                    <h4><font color="#FF0000" size="4">{ error_type }</font> in <a id="connect" href="" onclick="">{ log_path }</a>, 生成于12:30</h4>
                </td>
            </tr>
        </table>
    </div>"""

    error_type = "Fatal Exception"
    log_path = "/home/qinsw/downloads/android/log"

    f.write(title.format(logo="", error_type=error_type, log_path=log_path) + '\n\n')

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
    f.close()


def generate_results(task, data):
    """
    创建所有相关的文件
    :param task: 任务信息，主要是路径
    :param data: 经过解析，最终得到的数据
    """

    # 目录结构：
    # 第一级：
    #       文件：overview.html, overview_data.js,  logo.png
    #       目录： exceptions, signals
    # 第二级：
    #       exceptions：
    #           exceptions.html, exceptions.css, logo.png
    #       signals:
    #           signals.html, signals.css, logo.png

    num_exception = len(data[__M_JAVA__])
    num_signal = len(data[__M_NATIVE__])
    num_anr = len(data[__M_ANR__])
    result_path = task.log_path + "/Here"

    # 创建对应的目录
    try:
        os.makedirs(result_path, exist_ok=True)
    except OSError, e:
        tool.log(LOG_TAG, "create folder { %s } failed, reason: { %s }" % (result_path, e.message))
        return False

    # 判断并创建exceptions
    if num_exception > 0:
        generate_fatal_exception()

    # 判断并创建signals
    if num_signal > 0:
        generate_fatal_signal()

    # 创建overview
    # .1 创建overview_data.js
    create_overview_data()

    # .2 创建overview.html
    create_overview(result_path)


def generate_fatal_exception(folder, data):
    """
    创建Fatal Exception的html文件
    :param folder 指定的结果存放目录
    :param data: 存储着fatal exception的数据
    """

    # 1、路径
    exception_file = "fatal_exception.html"

    # 2、copy图片到指定路径

    # 3、copy css文件到指定路径

    # 4、创建html文件
    pass


def generate_fatal_signal(task, data):
    pass


def create_overview_data(folder, data):
    """
    在js文件夹下创建overview_data.js
    :param folder: 目录
    :param data:
    :return:
    """
    pass


def create_overview(folder):
    """
    根据主目录路径创建Overview网页文件
    :param folder:
    """
    overview_content = """
<!DOCTYPE HTML>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title id="head_title"></title>
    <style type="text/css"></style>
    <link rel='icon'
          href='data:image/x-icon;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABiElEQVQ4T6VTQVLCQBDsWVG8GfiAWmVyFV4gvAB/IFfJQXiB4QXAIXjFH8gLwB/knFglfgDiTRB3rE3Y1EbAKss9ZWene7pnJoR/HtqFt3qvFopfDUF8pt4l0wzLg3HcOY9/5ucIFFAU1/cA2nuE9eWy0DWJMgIFpqPPCRFVFJiBdwJOtr6ZA14d1jVJRlAaRlMCrrLKTAMp+EndhaRrEN/pNwami5ZdV/eEwHqIaoIxyRIYYxaFNj4Q4xhWkijXfSI0dI4k1ONbWxUFysNwBNDNRu5zAmBMzT4woQawRaDLNM6P85bTTAhKfjQjwqn6nrdsKvuRN3dtzyTQsfIw4gTOHCxcp7pRkAb/QqBzUwXDMNDSflMgV4W+KK4X2uqiZde2epDaQ3eXBRDUjmyO0YMdU4gZ3DF7QKAeUToRdSRzNXadINuDsv/SN2etVJgEuepMg7l7kWxrbpXNcebAuUsqXYe2fibLD5sE8vRYM8eMNwZ7seuM8tb2lLL8sAJBqWfJsfK7K/Ub4DK+EaJT/6MAAAAASUVORK5CYII='
          type=‘image/x-ico’/>
</head>
<body>
<script src="js/highcharts.js"></script>
<script src="js/exporting.js"></script>
<script src="js/overview_data.js"></script>
<div id="container"
     style="min-width: 800px; min-height: 450px; max-width: 1366px; max-height: 768px; marginTop: 100 auto">
</div>
<script type="text/javascript">
var head_title=document.getElementById("head_title");
head_title.innerHTML = Overview.head_title
var pieChart = Highcharts.chart('container', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.y}</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.y}',
                style: {
                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                }
            }
        }
    },
    colors: ['#ff5722', '#3f51b5', '#f15c80', '#00bcd4', '#009688', '#607d8b'],
    credits:{
    enabled: false  // 禁用版权信息
    }
});
pieChart.title.update({ text: Overview.chart_title })
var series1 = { name: 'Overview', colorByPoint: true, data: [] }
for(var i = 0; i < Overview.chart_data.length; i++) {
    var node = {}
    node['name'] = Overview.chart_data[i].name
    node['y'] = Overview.chart_data[i].y
    node['link'] = Overview.chart_data[i].link
    node['events'] = {
        click: function(event) {
            window.open(Overview.chart_data[this.index].link)
        }
    }
    if (i == 0) {
        node['sliced'] = true
        node['selected'] = true
    }
    series1.data.push(node)
}
pieChart.addSeries(series1)
</script>
</body>
</html>
"""
    overview_path = folder + "/" + "overview.html"
    overview = open(overview_path, "w")
    overview.write(overview_content)
    overview.close()



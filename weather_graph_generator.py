from pyecharts.charts import Map
from pyecharts.options import TitleOpts, VisualMapOpts
from weather_digester import pandas_extract_total_message
from constant import *

def get_graph_data_list():
    highest_temperature_dict = {}
    lowest_temperature_dict = {}

    raw_data = pandas_extract_total_message()
    for city, info_list in raw_data.items():
        city = chinese_fujian_cities_names[city]
        highest_temperature_dict[city] = [0.0, 0]
        lowest_temperature_dict[city] = [0.0, 0]
        info = info_list[0]
        for i in range(len(info[1])):
            highest_temperature_dict[city][0] += info[1][i]
            lowest_temperature_dict[city][0] += info[2][i]
            highest_temperature_dict[city][1] += 1
            lowest_temperature_dict[city][1] += 1

    highest_temperature_data_list = []
    lowest_temperature_data_list = []

    for city in highest_temperature_dict:
        value = highest_temperature_dict[city][0] / highest_temperature_dict[city][1]
        highest_temperature_data_list.append((f"{city}市", value))

        value = lowest_temperature_dict[city][0] / lowest_temperature_dict[city][1]
        lowest_temperature_data_list.append((f"{city}市", value))

    return lowest_temperature_data_list, highest_temperature_data_list


def set_global_opts_for_map(map, title):
    map.set_global_opts(
        title_opts=TitleOpts(title=title),
        visualmap_opts=VisualMapOpts(
            is_show=True,
            is_piecewise=True,
            pieces=[
                {"min": 0, "max": 5, "label": "0~5°C", "color": "rgb(0, 0, 255)"},  # 深蓝
                {"min": 5, "max": 10, "label": "6~10°C", "color": "rgb(65, 105, 225)"},  # 浅蓝
                {"min": 10, "max": 15, "label": "11~15°C", "color": "rgb(135, 206, 235)"},  # 很浅的蓝
                {"min": 15, "max": 20, "label": "16~20°C", "color": "rgb(205, 201, 153)"},  # 黄色
                {"min": 20, "max": 25, "label": "21~25°C", "color": "rgb(255, 192, 203)"},  # 浅红
                {"min": 25, "max": 30, "label": "26~30°C", "color": "rgb(255, 150, 162)"},  # 较深的浅红
                {"min": 30, "max": 35, "label": "31~35°C", "color": "rgb(255, 110, 120)"},  # 红
                {"min": 35, "max": 40, "label": "36~40°C", "color": "rgb(255, 0, 0)"}  # 红
            ]
        )
    )


def generate_map(title, data_list):
    map = Map()
    map.add(title, data_list, "福建")
    set_global_opts_for_map(map, title)
    return map.render_embed()


def get_html():
    lowest_temperature_data_list, highest_temperature_data_list = get_graph_data_list()
    lowest_html = generate_map("福建省7月平均最低气温分布", lowest_temperature_data_list)
    highest_html = generate_map("福建省7月平均最高气温分布", highest_temperature_data_list)

    # 创建HTML模板并插入图表代码
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        <div>{lowest_html}</div>
        <br>
        <br>
        <div>{highest_html}</div>
    </body>
    </html>
    """

    # 将HTML模板写入文件
    with open("福建省7月平均气温分布图.html", "w", encoding="utf-8") as f:
        f.write(html_template)

    return html_template


import os
import pandas
from constant import *
import weather_mapper

# 假设文件名为 'weather_data.txt'

def extract_line(line):
    # 去除引号并分割字符串
    line = line.strip('\n')
    parts = line.split(',')
    return parts


def pandas_extract_total_message():
    extracted_data = {}

    # 遍历所有城市
    for city_name in fujian_cities_abbreviations:
        file_name = f'{FEED_URI_ROOT}{city_name}.csv'

        # 读取 CSV 文件
        df = pandas.read_csv(file_name, encoding='utf-8')

        # 假设 CSV 文件中只有两列：city_name 和 weather
        # 使用 str.split 来分割 weather 列，逗号是分割符
        df[['date', 'highest_temperature', 'lowest_temperature', 'weather_type', 'wind']] = df['weather'].str.split(',',
                                                                                                                    expand=True)
        # 清洗数据：删除分割后容量与预期不符的行
        # 预期是日期、最高温度、最低温度、天气类型、风向风级，共5个部分
        df = df[df.apply(lambda row: not (
                    not (len(row['wind'].split(' ')) == 2) or
                    not is_temperature(row['highest_temperature']) or
                    not is_temperature(row['lowest_temperature'])
                    ), axis=1)]

        # 将清洗后的数据按城市存储
        extracted_data[city_name] = []
        new_row_dict = {}
        for key in df:
            new_row_dict[key] = []

            item_list = df[key]
            for i in range(len(df[key])):
                if key == 'highest_temperature' or key == 'lowest_temperature':
                    temperature_num = float(item_list[i][0:2])
                    new_row_dict[key].append(temperature_num)
                else:
                    new_row_dict[key].append(item_list[i])
        extracted_data[city_name].append((new_row_dict['date'],
                                          new_row_dict['highest_temperature'],
                                          new_row_dict['lowest_temperature'],
                                          new_row_dict['weather_type'],
                                          new_row_dict['wind']))

    return extracted_data


# 调用函数并打印结果
clean_data = pandas_extract_total_message()
# 清洗后的数据存到数据库中
weather_mapper.insert(clean_data)

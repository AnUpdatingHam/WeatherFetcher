import mysql.connector
from mysql.connector import Error
from constant import *

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'fujian_weather'
}

# 连接到 MySQL
connection = mysql.connector.connect(**db_config)


def insert(data):
    insert_query = ("insert into weather_data (city_name, date, highest_temperature,"
                    " lowest_temperature, weather_type, wind) values ")

    value_str_list = []

    for city, info_tuple in data.items():
        info = info_tuple[0]
        for i in range(len(info[0])):
            value_str_list.append(f"('{city}', "
                                  f"'{info[item_dict['date']][i][0:10]}', "
                                  f"{info[item_dict['highest_temperature']][i]}, "
                                  f"{info[item_dict['lowest_temperature']][i]}, "
                                  f"'{info[item_dict['weather_type']][i]}', "
                                  f"'{info[item_dict['wind']][i]}')")
    insert_query += ", ".join(value_str_list) + ";"

    cursor = connection.cursor()
    cursor.execute(insert_query)
    connection.commit()
    cursor.close()


def get_data(city):
    if city:
        select_query = (f"select city_name, date, highest_temperature,"
                        f" lowest_temperature, weather_type, wind from weather_data "
                        f"where city_name = '{city}'")
    else:
        select_query = ("select city_name, date, highest_temperature,"
                        " lowest_temperature, weather_type, wind from weather_data")

    cursor = connection.cursor()

    cursor.execute(select_query)
    data = cursor.fetchall()
    cursor.close()
    return data


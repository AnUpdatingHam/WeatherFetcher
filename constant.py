import re

# 配置Scrapy的输出
# 这里通常放在settings.py文件中，但为了整合到一个文件，我们直接在这里设置
FEED_FORMAT = 'csv'
FEED_URI_ROOT = './weather_data/'

fujian_cities_abbreviations = [
    'fuzhou',  # 福州
    'xiamen',  # 厦门
    'ningde',  # 宁德
    'putian',  # 莆田
    'quanzhou',  # 泉州
    'zhangzhou',  # 漳州
    'longyan',  # 龙岩
    'sanming',  # 三明
    'nanping'  # 南平
]

chinese_fujian_cities_names = {
    'fuzhou': '福州',
    'xiamen': '厦门',
    'ningde': '宁德',
    'putian': '莆田',
    'quanzhou': '泉州',
    'zhangzhou': '漳州',
    'longyan': '龙岩',
    'sanming': '三明',
    'nanping': '南平'
}

# 创建逆对应字典
english_fujian_cities_names = {value: key for key, value in chinese_fujian_cities_names.items()}

item_dict = {
    'date': 0,
    'highest_temperature': 1,
    'lowest_temperature': 2,
    'weather_type': 3,
    'wind': 4
}

def is_temperature(temperature):
    pattern = r'^[+-]?\d+℃$'
    # 使用 re.match 检查字符串是否符合正则表达式定义的模式
    if re.match(pattern, temperature):
        return True
    else:
        return False


import os
import scrapy
from scrapy import Request
import random
from bs4 import BeautifulSoup
from constant import *

class WeatherItem(scrapy.Item):
    city_name = scrapy.Field()
    weather = scrapy.Field()

class MyWeatherSpider(scrapy.Spider):
    name = 'my_weather_spider'
    allowed_domains = ['lishi.tianqi.com']
    city_name = '',

    headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) ...",  # 示例User-Agent
        # ... 其他User-Agent字符串
    ]

    def __init__(self, city_name='', *args, **kwargs):
        super(MyWeatherSpider, self).__init__(*args, **kwargs)
        self.city_name = city_name  # 接收并保存传入的参数

    def start_requests(self):
        url = f"http://lishi.tianqi.com/{self.city_name}/202407.html"
        yield Request(url=url, headers={'User-Agent': random.choice(self.headers)})

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.title
        # 获取<title>标签的文本，并提取前两个字
        # city_name = title_tag.string[:2]

        weather_list = response.css('ul.thrui')
        for weather in weather_list:
            ul_list = weather.css('li')
            for ul in ul_list:
                li_list = ul.css('div::text').getall()
                if li_list:
                    # 将提取的数据以字典形式返回
                    yield {
                        'city_name': city_name,
                        'weather': ','.join(li_list)
                    }


# 运行爬虫的代码通常不会放在爬虫文件中，但为了完整性，我将其包括在内
if __name__ == "__main__":
    # 检查文件是否存在，如果存在则删除
    # if os.path.exists(FEED_URI_ROOT):
    #     os.remove(FEED_URI_ROOT)
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess({
        'FEED_FORMAT': FEED_FORMAT,
    })

    for city_name in fujian_cities_abbreviations:
        # 构造每个城市的输出文件路径
        feeds = {}
        feed_uri = f"{FEED_URI_ROOT}{city_name}.{FEED_FORMAT}"
        feeds[feed_uri] = {'format': FEED_FORMAT}

        # 将字典添加到爬虫设置中
        process.settings.set('FEEDS', feeds, priority='spider')

        process.crawl(MyWeatherSpider, city_name=city_name)

    # 这里只调用一次 process.start()
    process.start()
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangchanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field() #标题
    internal_id = scrapy.Field() #网站内部id
    address = scrapy.Field() #地址
    unit_price = scrapy.Field() #当日均价
    build_time = scrapy.Field() #建造时间
    build_type = scrapy.Field() #建筑类型
    property = scrapy.Field() #物业公司
    property_fee = scrapy.Field() #物业费
    developer = scrapy.Field() #开发商
    # total_buildings = scrapy.Field() #楼栋数量
    # total_houses = scrapy.Field() #房屋数量
    plot_rate = scrapy.Field() #容积率
    green_rate = scrapy.Field() #绿化率
    parking_num = scrapy.Field() #停车位
    prices = scrapy.Field() #历史价格
    city = scrapy.Field()
    district = scrapy.Field()

    # # surrounding information item Field
    # lat = scrapy.Field() #纬度
    # lng = scrapy.Field() #经度
    # bus = scrapy.Field() #公交
    # subway = scrapy.Field() #地铁
    # school = scrapy.Field() #学校
    # hospital = scrapy.Field() #医院
    # commercial_area = scrapy.Field() #商圈
    # market_place = scrapy.Field() #商场
    pass

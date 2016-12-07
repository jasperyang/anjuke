# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from sqlalchemy import create_engine, Column, Integer, String, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .orm.entity import *
import uuid

class FangchanPipeline(object):
    def __init__(self, config):
        self.config = config

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            config = crawler.settings.get('DB_CONFIG')
        )

    def open_spider(self, spider):
        engine = create_engine('mysql+pymysql://%s:%s@localhost:3306/%s?charset=utf8' %
            (self.config.get('user'), self.config.get('password'), self.config.get('db')))
        DBsession = sessionmaker(bind=engine)
        self.session = DBsession()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        com = self.session.query(Community).filter(and_(Community.source == 'anjuke',Community.internal_id == item["internal_id"])).first()
        if not com:
            com_id = str(uuid.uuid1())
            com = Community(id = com_id,
                        source = "anjuke",
                        title = item["title"],
                        internal_id = item["internal_id"],
                        address = item["address"],
                        unit_price = item["unit_price"],
                        # prices = repr(item["prices"]),
                        # total_buildings = item["total_buildings"],
                        # total_houses = item["total_houses"],
                        build_type = item["build_type"],
                        build_time = item["build_time"],
                        developer = item["developer"],
                        property = item["property"],
                        property_fee = item["property_fee"],
                        parking_num = item["parking_num"],
                        green_rate = item["green_rate"],
                        plot_rate = item["plot_rate"],
                        city = item['city'],
                        district = item['district'])
            self.session.add(com)

        for i in range(0,len(item["prices"])-1):
            for k,v in item["prices"][i].items():
                price_id = str(uuid.uuid1())
                p = CommunityPriceHistory(id = price_id,
					source = "anjuke",
                                        community_id = com.id,
                                        month = k,
                                        price = v,)
                self.session.add(p)

        self.session.commit()
        return item

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('scraped_data_utf8.json','w',encoding='utf-8')

    def process_item(self,item,spider):
        line = json.dumps(item,ensure_ascii=False)+"\n"
        self.file.write(line)
        return item
    def spider_closed(self,spider):
        self.file.close()

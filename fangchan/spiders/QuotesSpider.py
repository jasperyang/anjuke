# -*- coding: utf-8 -*-
import scrapy
from json import *
import re
from fangchan.items import FangchanItem

start_url = "http://beijing.anjuke.com"

class QuotesSpider(scrapy.Spider):
    name = "anjuke"
    page_num = 0

    def start_requests(self):
        urls = [
            'http://beijing.anjuke.com/community/?from=esf_list_navigation',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for url in response.xpath("//div[@class='li-info']/h3/a/@href").extract():
            url = start_url + url
            yield scrapy.Request(url,callback=self.parse_details)


        next_page = response.xpath("//div[@class='multi-page']/a[@class=\"aNxt\"]/@href").extract()
        if(len(next_page) != 0):
            next_page = next_page[0]

        print(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def judge_empty(self,string):
        if(string == '暂无数据'):
            return False
        return True

    def parse_details(self,response):
        item = FangchanItem()

        #匹配年份数据
        #打注释的都是存成json格式需要用到的代码

        m = response.xpath("//script[contains(.,'priceTrend')]/text()").extract()
        if(len(m) != 0):
            m = m[0].encode('utf-8')
            m = m.decode('GBK')
            re2 = re.findall('community : ([\[\]{},0-9":\n]*)',m)
            d = JSONDecoder().decode(re2[0][:-2])
            item['prices'] = d;
        #data = {'data':d}
        #匹配基本信息
        #dt = response.xpath("//dl[@class='comm-l-detail float-l']/dt/text()").extract()
        dd = response.xpath("//dl[@class='comm-l-detail float-l']/dd/text()").extract()
        tmp = response.xpath("//em[@class='comm-avg-price']/text()").extract()
        place = response.xpath("//*[@id='content']/div[6]/div[3]/div[1]/dl[1]/dd[2]/a[1]/@title").extract()
        district = response.xpath("//*[@id='content']/div[6]/div[3]/div[1]/dl[1]/dd[2]/a[2]/@title").extract()
        if len(tmp) != 0:
            item['unit_price'] = int(tmp[0])
        item['title'] = dd[0]
        address = response.xpath('//*[@id="content"]/div[6]/div[3]/div[1]/dl[1]/dd[3]/em/text()').extract()
        if len(address) != 0:
            item['address'] = address[0]
        item['developer'] = dd[3]
        item['city'] = "北京"
        item['district'] = place[0] + "  " + district[0]
        item['property'] = dd[4]
        item['build_type'] = dd[5]
        item['property_fee'] = dd[6]
        bankuai = ''
        #dt2 = response.xpath("//dl[@class='comm-r-detail float-r']/dt/text()").extract()
        dd2 = response.xpath("//dl[@class='comm-r-detail float-r']/dd/text()").extract()
        # item['total_buildings'] = 'null'
        # item['total_houses'] = 'null'
        item['build_time'] = dd2[2]
        item['plot_rate'] = dd2[3]
        item['green_rate'] = dd2[6]
        item['parking_num'] = dd2[5]
        # for ban in response.xpath("//dl[@class='comm-l-detail float-l']/dd/a/@title").extract():
        #     bankuai = bankuai + ban+' '
        # dizhi = response.xpath("//dl[@class='comm-l-detail float-l']/dd/em/text()").extract()[0]
        # details = dict(zip(dt,dd))
        # details2 = dict(zip(dt2,dd2))
        # details[u'\u6240\u5728\u7248\u5757'] = bankuai
        # details[u'\u5730\u5740'] = dizhi
        # detail = dict(details.items() + details2.items() + data.items())
        a = response.xpath("//link[@rel='canonical']/@href").extract()
        r = re.findall("[0-9].*",a[0])
        item["internal_id"] = r
        yield item
        #yield detail




# -*- coding: utf-8 -*-
import scrapy
from json import *
import re
from fangchan.items import FangchanItem


class QuotesSpider(scrapy.Spider):
    name = "anjuke"
    page_num = 0

    def start_requests(self):
        start_url = 'http://www.anjuke.com/sy-city.html'
        yield scrapy.Request(url=start_url,callback=self.parse_district)

    #按照不同的城市抓取
    def parse_district(self, response):

        #left
        for i in range(1,len(response.xpath('//*[@id="content"]/div[4]/div[1]/dl').extract())):
            print(i)
            pattern = '//*[@id="content"]/div[4]/div[1]/dl[%d]/dd/a/@href' % i
            url = response.xpath(pattern).extract()
            for j in range(len(url)):
                print(url[j])
                uri = url[j] + '/community/'
                yield scrapy.Request(url=uri, meta={"city": url[j].split('.')[0][7:],"url_prefix":url}, callback=self.parse_block)

        #right
        for i in range(1, len(response.xpath('//*[@id="content"]/div[4]/div[2]/dl').extract())):
            print(i)
            pattern = '//*[@id="content"]/div[4]/div[2]/dl[%d]/dd/a/@href' % i
            url = response.xpath(pattern).extract()
            for j in range(len(url)):
                print(url[j])
                uri = url[j] + '/community/'
                yield scrapy.Request(url=uri, meta={"city": url[j].split('.')[0][7:],"url_prefix":url}, callback=self.parse_block)

        #rest
        for url in response.xpath('//*[@id="otherCity"]/dl/dd/a/@href').extract():
            print(url)
            uri = url + '/community/'
            yield scrapy.Request(url=uri, meta={"city": url.split('.')[0][7:],"url_prefix":url}, callback=self.parse_block)
            break

    #解析每个城市的板块
    def parse_block(self,response):
        city = str(response.meta['city'])
        print(city)
        for block_url in response.xpath('//span[@class="elems-l"]/a/@href').extract():
            yield scrapy.Request(url=block_url,meta={"city":city,"url_prefix":response.meta["url_prefix"]},callback=self.parse_dist)

    def parse_dist(self,response):
        city = str(response.meta['city'])
        print(city)
        for district_url in response.xpath('//div[@class="sub-items"]/a/@href').extract():
            yield scrapy.Request(url=district_url, meta={"city":city,"url_prefix":response.meta["url_prefix"]}, callback=self.parse)

    #每个城市具体的分析
    def parse(self, response):
        city = str(response.meta['city'])
        for url in response.xpath("//div[@class='li-info']/h3/a/@href").extract():
            url = response.meta["url_prefix"] + url
            yield scrapy.Request(url,meta={"city":city},callback=self.parse_details)

        next_page = response.xpath("//div[@class='multi-page']/a[@class=\"aNxt\"]/@href").extract()
        if(len(next_page) != 0):
            next_page = next_page[0]

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
        if len(tmp) != 0 and tmp != '暂无均价':
            item['unit_price'] = int(tmp[0])
        if len(dd) != 0:
            item['title'] = dd[0]
        address = response.xpath('//*[@id="content"]/div[6]/div[3]/div[1]/dl[1]/dd[3]/em/text()').extract()
        if len(address) != 0:
            item['address'] = address[0]
        item['developer'] = dd[4]
        item['city'] = response.meta["city"]
        if len(place) != 0 and len(district) != 0:
            item['district'] = place[0] + "  " + district[0]
        item['property'] = dd[5]
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




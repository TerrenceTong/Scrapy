# -*- coding: utf-8 -*-
import scrapy
import re
import os
import requests

#导入链接规则匹配
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from maoyan.get_realtext import get_realtext
#导入模板
from maoyan.items import MaoyanItem

from fontTools.ttLib import TTFont

count = 0

class MyspiderSpider(CrawlSpider):
    # 请求头设置
    header = {
    'Accept': '*/*;',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'maoyan.com',
    'Referer': 'http://maoyan.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    name = 'myspider'
    allowed_domains = ['maoyan.com']
    #start_urls = ['https://maoyan.com/films?showType=3&sortId=3&yearId=14&offset=0']
    #start_urls = ['https://maoyan.com/films?showType=3&sortId=3&yearId=13&offset=0']
    #start_urls = ['https://maoyan.com/films?showType=3&sortId=3&yearId=12&offset=0']
    #start_urls = ['https://maoyan.com/films?showType=3&sortId=3&yearId=11&offset=0']
    start_urls = ['https://maoyan.com/films?showType=3&sortId=3&yearId=10&offset=1650']
    rules = (
        Rule(LinkExtractor(allow=r'offset=\d+'),follow=True),
        Rule(LinkExtractor(allow=r'/films/\d+'),callback='parse_maoyan',follow=False),
    )


    def parse_maoyan(self, response):
        item = MaoyanItem()
        #pattern = re.compile(r'\"movieId\"\:\"[0-9]+\"')
        id_str = response.xpath('/html/body/div[3]/div/div[2]/div[2]/div/@data-val').extract()[0]
        item['id'] = id_str.split(':')[1].rstrip('}')
        # 影片中文名称/英文名称
        item['ztitle'] = response.xpath('//h3/text()').extract()[0]
        #item['etitle'] = response.xpath('//div[@class="ename ellipsis"]/text()').extract()[0]
        # 上映时间
        item['release_time'] = response.xpath('//li[@class="ellipsis"][3]/text()').extract()[0]
        # 国家和地区
        item['mv_country'] = response.xpath('//li[@class="ellipsis"][2]/text()').extract()[0].split()[0]
        # 导演
        item['mv_director'] = response.xpath('//a[@class="name"]/text()').extract()[0].strip()

        # 主演
        star_1 = response.xpath('//li[@class="celebrity actor"][1]//a[@class="name"]/text()').extract()[0].strip()
        star_2 = response.xpath('//li[@class="celebrity actor"][2]//a[@class="name"]/text()').extract()[0].strip()
        star_3 = response.xpath('//li[@class="celebrity actor"][3]//a[@class="name"]/text()').extract()[0].strip()
        item['mv_star'] = star_1 + "\\" + star_2 + '\\' +star_3
        
        # 编剧
        item['mv_scriptwriter'] = response.xpath('//li[@class="celebrity "][1]//a[@class="name"]/text()').extract()[0].strip()

        # 图片链接
        item['mv_image'] = response.xpath('//img[@class="avatar"]/@src').extract()[0]

        # 影片时间
        #item['time'] = response.xpath('//li[@class="ellipsis"][2]/text()').extract()[0].strip()[-5:]

        # 评分
        result = get_realtext.web(response.url)
        item['mv_score'] = result[0]
        
        # 评论人数
        item['mv_numbers'] = result[1]

        # 简介
        item['mv_introduction'] = response.xpath('//span[@class="dra"]/text()').extract()[0].strip()

        # 影片类型
        item['mv_type'] = response.xpath('//li[@class="ellipsis"][1]/text()').extract()[0]
 
        yield item
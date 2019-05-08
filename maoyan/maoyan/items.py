# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = scrapy.Field()

    #影片中文名称/英文名称
    ztitle = scrapy.Field()
    #etitle = scrapy.Field()

    #上映时间
    release_time = scrapy.Field()

    #国家
    mv_country = scrapy.Field()

    #导演
    mv_director = scrapy.Field()

    #主演
    mv_star = scrapy.Field()

    #编剧
    mv_scriptwriter = scrapy.Field()

    #图片链接
    mv_image = scrapy.Field()

    #评分
    mv_score = scrapy.Field()

    #评论人数
    mv_numbers = scrapy.Field()
    
    #简介
    mv_introduction = scrapy.Field()

    #影片类型
    mv_type = scrapy.Field()
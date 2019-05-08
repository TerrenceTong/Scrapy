# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

""" mysql--version:8.0.15 """

import json
import pymysql.cursors

class MaoyanPipeline(object):
    def __init__(self):
        #连接数据库
        self.connect = pymysql.connect(
            #host = '118.24.214.240',
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'spider',
            charset = 'utf8'  # 别写成utf-8
            )
        self.cursor = self.connect.cursor()  # 建立游标
        #self.filename = open('maoyan.txt','wb')
 
    def process_item(self, item, spider):
        """ text = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.filename.write(text.encode('utf-8'))
        return item """
        item = dict(item)
        sql = "insert into all_info(id,ztitle,release_time,mv_country,mv_director,mv_star,mv_scriptwriter,mv_image,mv_score,mv_numbers,mv_introduction,mv_type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql,(item['id'],item['ztitle'],item['release_time'],item['mv_country'],item['mv_director'],item['mv_star'],item['mv_scriptwriter'],item['mv_image'],item['mv_score'],item['mv_numbers'],item['mv_introduction'],item['mv_type'],))
        self.connect.commit()
        return item

    def close_spider(self,spider):
        #self.filename.close()
        self.cursor.close()
        self.connect.close()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class WeibocrawlPipeline(object):
    def __init__(self):
        self.conn=pymysql.connect(host="127.0.0.1",user="root",passwd="dasharea",db="hexun",charset="utf8")
    def process_item(self, item, spider):
        for i in range(0,len(item['name'])):
            name=item['name'][i]
            url=item['url'][i]
            hits=item['hits'][i]
            comment=item['comment'][i]
            sql="insert into myhexun(name,url,hits,comment) VALUES('"+name+"','"+url+"','"+hits+"','"+comment+"')"
            self.conn.query(sql)
            # cur=self.conn.cursor()
            # cur.execute("""insert into 'myhexun'('name','url','hits','comment') values (%s,%s,%s,%s)""",(name,url,hits,comment))
            self.conn.commit()


        return item

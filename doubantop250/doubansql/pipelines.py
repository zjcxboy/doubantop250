# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from doubansql import settings
import pymysql
class DoubansqlPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
    def process_item(self, item, spider):
        self.cursor.execute(
            """insert into doub_doubdata(moviename,dbimgurl,classname,grade,count,introduction) values(%s,%s,%s,%s,%s,%s)""",
            (item['moviename'],
             item['dbimgurl'],
             item['classname'],
             item['grade'],
             item['count'],
             item['introduction']
             ))
        # 执行sql语句，item里面定义的字段和表字段一一对应
        self.connect.commit()
        # 提交
        return item
        # 返回item

    def close_spider(self, spider):
        self.cursor.close()
        # 关闭游标
        self.connect.close()
        # 关闭数据库连接

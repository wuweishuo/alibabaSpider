# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AlibabaPipeline(object):
    def process_item(self, item, spider):
        return item


import pymysql
from alibaba import settings


class CompanyPipeline(object):
    def __init__(self):
        # 连接数据库
        self.client = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        if spider.name == 'company':
            try:
                # 插入数据
                self.cursor.execute(
                    "insert into company(name, url, cat, ccat ,mainProducts, region, totalRevenue, top3Markets) value (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (item['name'],
                     item['url'],
                     item['cat'],
                     item['ccat'],
                     item['mainProducts'],
                     item['region'],
                     item['totalRevenue'],
                     item['top3Markets']))

                # 提交sql语句
                self.connect.commit()

            except Exception as error:
                # 出现错误时打印错误日志
                print(error)
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.client.close()

class ContactPipeline(object):

    def process_item(self, item, spider):
        if spider.name == 'contact':
            try:
                # 插入数据
                spider.cur.execute(
                    "insert into guangzhou_contact(id, name, department, job ,telephone, mobilephone, fax, address ,zip, country, province, city) value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (item.get("id"),
                     item.get("name", ""),
                     item.get("department", ""),
                     item.get("job", ""),
                     item.get("telephone", ""),
                     item.get("mobilePhone", ""),
                     item.get("fax", ""),
                     item.get("address", ""),
                     item.get("zip", ""),
                     item.get("country", ""),
                     item.get("province", ""),
                     item.get("city", "")))

                # 提交sql语句
                spider.client.commit()

            except Exception as error:
                # 出现错误时打印错误日志
                print(error)
        return item


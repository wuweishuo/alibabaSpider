# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AlibabaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = scrapy.Field()
    url = scrapy.Field()
    cat = scrapy.Field()
    ccat = scrapy.Field()
    mainProducts = scrapy.Field()
    region = scrapy.Field()
    totalRevenue = scrapy.Field()
    top3Markets = scrapy.Field()
    pass


class ContactItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    department = scrapy.Field()
    job = scrapy.Field()
    telephone = scrapy.Field()
    mobilePhone = scrapy.Field()
    fax = scrapy.Field()
    address = scrapy.Field()
    zip = scrapy.Field()
    country = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()


class errUrlItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()

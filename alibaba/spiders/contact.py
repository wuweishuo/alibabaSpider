# -*- coding: utf-8 -*-
import scrapy
import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy import signals
from pydispatch import dispatcher
from alibaba import settings
from alibaba.items import ContactItem
import logging


class ContactSpider(scrapy.Spider):
    name = 'contact'
    allowed_domains = ['www.alibaba.com']
    start_urls = []

    count = 1000

    def __init__(self):
        # selenium
        # options = Options()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # options.add_experimental_option("prefs", prefs)
        # options.headless = True
        # driver_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\chromedriver.exe"
        # print(driver_path)
        # 创建Firefox浏览器的一个Options实例对象
        profile = webdriver.FirefoxProfile()
        # 禁用CSS加载
        profile.set_preference('permissions.default.stylesheet', 2)
        # 禁用images加载
        profile.set_preference('permissions.default.image', 2)
        # 禁用flash插件
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = True
        profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        self.browser = webdriver.Firefox(executable_path=settings.FIREFOX_WEBDRIVER_PATH,
                                         firefox_profile=profile, firefox_options=fireFoxOptions)
        # mysql
        self.client = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8'
        )
        self.cur = self.client.cursor()
        # startUrls
        sql = "select id,url from company where name like '%guangzhou%' and id <= {} and id > {}".format(settings.END, settings.START)
        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
            for url in results:
                id = url[0]
                contact_url = url[1]  # type: str
                if not (contact_url.startswith("http:") or contact_url.startswith("https:")):
                    contact_url = "https:" + contact_url
                if not (contact_url.endswith("/")):
                    contact_url += "/"
                contact_url += ("contactinfo.html?%d" % (id))
                self.start_urls.append(contact_url)
        except Exception as error:
            logging.error("contact spider init err:{}".format(error))
        # 关闭资源
        dispatcher.connect(receiver=self.spiderCloseHandler, signal=signals.spider_closed)

    def spiderCloseHandler(self, spider):
        self.browser.quit()
        self.cur.close()
        self.client.close()

    def parse(self, response):
        id = response.meta.get("id")
        item = ContactItem()
        item['id'] = id
        name = response.css(".contact-name::text").extract_first()
        if not name:
            name = response.css(".contact-info .name::text").extract_first()
            if name:
                name = name.strip()
        item['name'] = name
        department = response.css(".contact-department::text").extract_first()
        job = response.css(".contact-job::text").extract_first()
        if not (department and job):
            dds = response.css(".contact-info .dl-horizontal dd::text")
            dts = response.css(".contact-info .dl-horizontal dt::text")
            if dds:
                for i in range(len(dds)):
                    dd = dds[i].extract()
                    dt = dts[i].extract()
                    if dt == 'Department:':
                        department = dd
                    elif dt == 'Job Title:':
                        job = dd
        item['department'] = department
        item['job'] = job
        info_table = response.css(".info-table tr")
        if info_table:
            for info in info_table:
                th = info.css("th::text").extract_first()
                td = info.css("td::text").extract_first()
                if th == 'Telephone:':
                    item['telephone'] = td
                elif th == 'Mobile Phone:':
                    item['mobilePhone'] = td
                elif th == 'Fax:':
                    item['fax'] = td
                elif th == 'Address:':
                    item['address'] = td
                elif th == 'Zip:':
                    item['zip'] = td
                elif th == 'Country/Region:':
                    item['country'] = td
                elif th == 'Province/State:':
                    item['province'] = td
                elif th == 'City:':
                    item['city'] = td
        else:
            item['telephone'] = response.css(
                ".contact-detail .sensitive-info .dl-horizontal dd[data-role=phone]::text").extract_first()
            item['mobilePhone'] = response.css(
                ".contact-detail .sensitive-info .dl-horizontal dd[data-role=mobile]::text").extract_first()
            item['fax'] = response.css(
                ".contact-detail .sensitive-info .dl-horizontal dd[data-role=fax]::text").extract_first()
            dds = response.css(".contact-detail .public-info .dl-horizontal dd::text").extract()
            dts = response.css(".contact-detail .public-info .dl-horizontal dt::text").extract()
            for i in range(len(dts)):
                dt = dts[i]
                dd = dds[i]
                if dt == 'Address:':
                    item['address'] = dd
                elif dt == 'Zip:':
                    item['zip'] = dd
                elif dt == 'Country/Region:':
                    item['country'] = dd
                elif dt == 'Province/State:':
                    item['province'] = dd
                elif dt == 'City:':
                    item['city'] = dd

        yield item

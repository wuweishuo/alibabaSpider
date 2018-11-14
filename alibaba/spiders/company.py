# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from alibaba.items import CompanyItem


class CompanySpider(scrapy.Spider):
    name = 'company'
    allowed_domains = ['www.alibaba.com']
    start_urls = ['https://www.alibaba.com/companies']

    # 爬取大的分类信息
    def parse(self, response):
        categorys = response.css(".ui-box.ui-box-normal.ui-box-wrap.clearfix .g-cate-list dl dt a")
        for cat in categorys:
            name = cat.css("::text").extract_first()
            url = cat.css("::attr(href)").extract_first()
            yield scrapy.Request(url, callback=self.parseCategory, meta={'cat': name})
        pass

    # 爬取详细分类信息
    def parseCategory(self, response):
        cat = response.meta['cat']
        ccats = response.css("#category-main-box .g-float-left>ul>li>a")
        for ccat in ccats:
            name = ccat.css("::text").extract_first()
            url = ccat.css("::attr(href)").extract_first()
            ccat_url = urljoin(self.start_urls[0], url)
            yield scrapy.Request(ccat_url, callback=self.parseCompany, meta={'ccat': name, 'cat': cat})
        pass

    def parseCompany(self, response):
        cat = response.meta['cat']
        ccat = response.meta['ccat']

        # 爬取下一页
        next_url = response.css(".next::attr(href)").extract_first()
        if (next_url):
            yield scrapy.Request(urljoin(response.url, next_url), callback=self.parseCompany, meta={'cat': cat, 'ccat': ccat})

        # 爬取公司信息
        items = response.css(".item-main")
        for item in items:
            company = CompanyItem()
            title = item.css(".item-title .title.ellipsis a")
            company["name"] = title.css("::text").extract_first().strip()
            url = title.css("::attr(href)").extract_first()
            url = url.rpartition("/")[0]
            company["url"] = url
            attrs = item.css(".content.util-clearfix .right .attr")
            for attr in attrs:
                name = attr.css(".name::text").extract_first()
                value = attr.css(".value")
                if name == 'Main Products:':
                    mainProducts = value.css("::text").extract_first()
                    company["mainProducts"] = mainProducts
                elif name == "Country/Region:":
                    region = value.css(".ellipsis.search::text").extract_first()
                    company["region"] = region
                elif name == "Total Revenue:":
                    totalRevenue = value.css(".ellipsis.search::text").extract_first()
                    company["totalRevenue"] = totalRevenue
                elif name == "Top 3 Markets:":
                    top3 = value.css(".ellipsis.search::text").extract()
                    company["top3Markets"] = ",".join(top3)
            company["ccat"] = ccat
            company["cat"] = cat
            yield company
        pass
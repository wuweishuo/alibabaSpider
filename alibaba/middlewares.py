# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class AlibabaSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AlibabaDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


from scrapy import Request
class ContactDownloaderMiddleware(object):

    def process_request(self, request, spider):
        if spider.name == 'contact':
            url = request.url
            list = url.split("?")
            if(len(list) > 1):
                url = list[0]
                id = list[1]
                return Request(url=url, meta={"id": id})
        return None


import time
import logging
from scrapy.http import HtmlResponse


class SeleniumDownloaderMiddleware(object):

    def process_request(self, request, spider):
        if spider.name == 'contact':
            try:
                url = request.url
                spider.browser.get(url)
                time.sleep(1)
                if self.is_element_exist(".sens-mask .icbu-link-default", spider.browser):
                    viewButton = spider.browser.find_element_by_css_selector(".sens-mask .icbu-link-default")
                elif self.is_element_exist(".contact-detail-mask .view-contact-trigger", spider.browser):
                    viewButton = spider.browser.find_element_by_css_selector(".contact-detail-mask .view-contact-trigger")
                if viewButton:
                    spider.browser.execute_script("arguments[0].click();", viewButton)
                # spider.browser.execute_script("arguments[0].scrollIntoView();", viewButton)
                time.sleep(2)
                if self.is_element_exist(".sc-hd-prefix2-dialog-bd", spider.browser):
                    spider.browser.execute_script("arguments[0].click();", spider.browser.find_element_by_css_selector(".sc-hd-prefix2-tab-trigger"))
                    time.sleep(1)
                    spider.browser.switch_to.frame("alibaba-login-box")
                    spider.browser.find_element_by_id("fm-login-id").send_keys("your username")
                    time.sleep(1)
                    spider.browser.find_element_by_id("fm-login-password").send_keys("your password")
                    time.sleep(1)
                    # submit = spider.browser.find_element_by_id("fm-login-submit")
                    spider.browser.execute_script("document.getElementById('fm-login-submit').click();")
                    # spider.browser.execute_script("arguments[0].scrollIntoView();", submit)
                    # submit.click()
                    time.sleep(5)
                    spider.browser.switch_to.default_content()
            except Exception as error:
                logging.error("{} err:{}".format(url, error))
            return HtmlResponse(spider.browser.current_url, body=spider.browser.page_source, encoding='utf-8',
                                request=request)
        return None

    def is_element_exist(self, css, browser):
        s = browser.find_elements_by_css_selector(css_selector=css)
        if len(s) == 0:
            return False
        elif len(s) == 1:
            return True
        else:
            return False

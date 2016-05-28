from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, HtmlResponse, FormRequest
from scrapy.utils.spider import iterate_spider_output
from scrapy.spiders import Spider
from webcrawler.items import URLItem
import urlparse
import logging



# Test DVWA IP address is 192.168.57.30
# Change the IP address if tested in new environment


class CKSpider(CrawlSpider):

    name = 'dvwa_login'

    form_username = 'username'
    form_password = 'password'
    username = 'admin'
    password = 'password'

    allowed_domains = ['192.168.57.30']

    login_page = 'http://192.168.57.30/login.php'

    start_urls = ['http://192.168.57.30/index.php',]

    rules = [
        Rule(
            LinkExtractor(  allow=(), 
                            deny=('/logout*')), 
            callback="parse_item", 
            follow=True)
        ]

    def start_requests(self):
        logging.debug("start send request")
        yield Request(url=self.login_page, callback=self.login, dont_filter=True)

    def login(self, response):
        logging.debug("submit login ")
        yield FormRequest.from_response(response, 
                                         formdata={self.form_username: self.username, self.form_password: self.password},
                                         callback=self.check_login_response)

    def check_login_response(self, response):
        if "logout" in response.body:
            logging.debug("finish login")
            return self.parse(response)


    def parse(self, response):
        logging.debug("run parse item")
        yield self.parse_item(response)
        logging.debug("run parse")
        parsed_response = self._parse_response(response, self.parse_start_url, cb_kwargs={}, follow=True)
        for requests_or_item in parsed_response:
            logging.debug("\nrequest or item after log in: \n")
            logging.debug(requests_or_item)
            yield requests_or_item


    def parse_item(self, response):

        url_obj = urlparse.urlsplit(response.url)
        url_ret = urlparse.urlunsplit((url_obj.scheme, url_obj.netloc, url_obj.path, '', ''))

        item = URLItem()
        item['url_base'] = url_ret
        item['url_parameters'] = url_obj.query

        return item










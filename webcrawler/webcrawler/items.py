# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class URLItem(scrapy.Item):
    url_base = scrapy.Field()
    outLinks = scrapy.Field()
    url_parameters = scrapy.Field()
    forms = scrapy.Field()


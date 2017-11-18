# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingyouItem(scrapy.Item):
    # define the fields for your item here like:
    ques = scrapy.Field()
    answer = scrapy.Field()

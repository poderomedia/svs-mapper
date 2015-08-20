# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class Directory(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    type = Field()
    company_ICN = Field()
    company_name = Field()
    person_ICN = Field()
    person_name = Field()
    person_jobtitle = Field()
    person_jobtitle_desc = Field()
    person_datejob = Field()
    person_datejob_end = Field()
    scanner_date = Field()
    reference = Field()


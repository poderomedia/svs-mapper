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
    doc_ext_id = Field()
    doc_date = Field()
    doc_desc = Field()
    type = Field()
    company_ICN = Field()
    company_name = Field()
    company_active = Field()
    company_admin = Field()
    person_ICN = Field()
    person_name = Field()
    person_jobtitle = Field()
    person_jobtitle_desc = Field()
    person_datejob = Field()
    person_datejob_end = Field()
    scanner_date = Field()
    reference = Field()
    doc_url = Field()

    #stock holders
    stock_date = Field()
    stock_name = Field()
    stock_percentage = Field()


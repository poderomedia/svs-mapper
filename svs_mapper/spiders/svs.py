# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from svs_mapper.items import Directory
from scrapy.http import Request
from datetime import date
import hashlib


class SvsSpider(scrapy.Spider):
    name = "svs"
    allowed_domains = ["svs.cl"]
    base_url = 'http://www.svs.cl/institucional/mercados/'
    start_urls = [
        'http://www.svs.cl/institucional/mercados/listado_actual_directorios.php?mercado=V',
        'http://www.svs.cl/institucional/mercados/listado_actual_directorios.php?mercado=S'
    ]
    today = date.today()

    def parse(self, response):

        hxs = Selector(response)

        company_list = hxs.xpath('//tr[td]')

        for item in company_list:
            data = Directory()
            data['company_ICN'] = ''.join(item.xpath('td[1]/a/text()').extract()).strip()
            data['type'] = 'Board'
            data['company_name'] = ''.join(item.xpath('td[2]/a/text()').extract()).strip()
            link = ''.join(item.xpath('td[2]/a/@href').extract()).strip()
            request = Request(self.base_url + link,
                              callback = self.parse_details,
                              meta = {'data':data}
                              )
            yield request

    def parse_details(self,response):

        hxs = Selector(response)
        data = response.meta['data']

        jobtitles_list = hxs.xpath('//tr[td]')

        for item in jobtitles_list:
            data['person_ICN'] = ''.join(item.xpath('td[1]/text()').extract()).strip()
            data['person_name'] = ''.join(item.xpath('td[2]/text()').extract()).strip()
            data['person_jobtitle'] = ''.join(item.xpath('td[3]/text()').extract()).strip()
            data['person_datejob'] = ''.join(item.xpath('td[4]/text()').extract()).strip()
            #default value -1 to indicate "to present time"
            data['person_datejob_end'] = '-1'
            data['scanner_date'] = self.today
            m = hashlib.md5()
            to_hash = data['type'] + data['company_ICN'] + data['company_name'] + \
                      data['person_ICN'] + data['person_name'] + data['person_datejob'] +\
                      data['person_datejob_end'] + data['person_jobtitle']
            m.update(to_hash.encode('utf-8'))
            data['id'] = m.hexdigest()
            data['reference'] = response.url
            yield data

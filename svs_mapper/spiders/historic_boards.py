# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, Spider
from svs_mapper.items import Directory
from scrapy.http import Request
from datetime import date
import hashlib
import time


class HistoricBoardsSpider(Spider):
    name = "historic_boards"
    allowed_domains = ["svs.cl"]
    letters = map(chr, range(97, 123))
    letters.append(['ñ','á','é','í','ó','ú'])
    start_urls = [
        'http://www.svs.cl/institucional/mercados/reporte_ejecutivos.php?tipo=texto&mercado=V&criterio=%s' % letter
        for letter in letters
    ]
    base_url = 'http://www.svs.cl/institucional/mercados/'
    today = date.today()

    def parse(self, response):

        hxs = Selector(response)
        h_list = hxs.xpath('//tr[td]')
        for item in h_list:
            director = Directory()
            director['person_ICN'] = ''.join(item.xpath('td[1]/a/text()').extract()).strip()
            director['person_name'] = ''.join(item.xpath('td[2]/a/text()').extract()).strip()
            #director['type'] = 'Board'
            link = self.base_url + ''.join(item.xpath('td[2]/a/@href').extract()).strip()
            request = Request(link,
                              callback = self.parse_details,
                              meta = {'director':director}
                              )
            yield request

    def parse_details(self,response):

        hxs = Selector(response)

        director = response.meta['director']
        jobtitles_list = hxs.xpath('//tr[td]')
        for item in jobtitles_list:
            director['company_ICN'] = ''.join(item.xpath('td[1]/text()').extract()).strip()
            director['company_name'] = ''.join(item.xpath('td[2]/text()').extract()).strip()
            director['person_jobtitle'] = ''.join(item.xpath('td[3]/text()').extract()).strip()
            director['type'] = 'Executive'
            if ('Director' in director['person_jobtitle']) | ('Presidente' in director['person_jobtitle'])\
                    | ('Vicepresidente' in director['person_jobtitle']):
                director['type'] = 'Board'

            director['person_jobtitle_desc'] = ''.join(item.xpath('td[4]/text()').extract()).strip()

            #date object INI
            date_str = ''.join(item.xpath('td[5]/text()').extract()).strip()
            date_struct = time.strptime(date_str,'%d/%m/%Y')
            director['person_datejob'] = time.strftime('%Y-%m-%dT%H:%M:%SZ',date_struct)

            #date object END
            date_str_end = ''.join(item.xpath('td[6]/text()').extract()).strip()
            if date_str_end != '':
                date_struct_end = time.strptime(date_str_end,'%d/%m/%Y')
                director['person_datejob_end'] = time.strftime('%Y-%m-%dT%H:%M:%SZ',date_struct_end)
            else:
                director['person_datejob_end'] = 'NOW'

            director['scanner_date'] = self.today.strftime('%Y-%m-%dT%H:%M:%SZ')
            m = hashlib.md5()
            to_hash = director['type'] + director['company_ICN'] + director['company_name'] + \
                      director['person_ICN'] + director['person_name'] + director['person_datejob'] +\
                      director['person_datejob_end'] + director['person_jobtitle']
            m.update(to_hash.encode('utf-8'))
            director['id'] = m.hexdigest()
            director['reference'] = response.url
            yield director

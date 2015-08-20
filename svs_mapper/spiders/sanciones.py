# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, Spider
from svs_mapper.items import Directory
from scrapy.http import Request
from datetime import date
import hashlib

class SancionesSpider(Spider):
    name = "sanciones"
    allowed_domains = ["svs.cl"]
    base_url_query = 'http://www.svs.cl/institucional/sanciones/sanciones_cursadas_anteriores.php?' \
                     'desde=%s&rut=&vig=&hasta=%s'
    base_url = 'http://www.svs.cl'
    start_urls = []
    today = date.today()

    def __init__(self,date_ini='01-01-2001', date_end=str(date.today().strftime('%d-%m-%Y')),*args, **kwargs):
        self.start_urls = [self.base_url_query % (date_ini,date_end)]

    def parse(self, response):

        hxs = Selector(response)

        sanctions_list = hxs.xpath('//tr[td]')

        for document in sanctions_list:
            data = Directory()
            data['type'] = 'Sanctions'
            data['doc_ext_id'] = ''.join(document.xpath('td[1]/text()').extract()).strip()
            data['doc_date'] = ''.join(document.xpath('td[2]/text()').extract()).strip()
            data['doc_desc'] = ''.join(document.xpath('td[3]/text()').extract()).strip()
            data['doc_url'] = self.base_url + ''.join(document.xpath('td[4]/a/@href').extract()).strip()
            m = hashlib.md5()
            to_hash = data['type'] + data['doc_ext_id'] + data['doc_date'] + data['doc_url']
            m.update(to_hash.encode('utf-8'))
            data['id'] = m.hexdigest()
            data['scanner_date'] = self.today
            data['reference'] = response.url
            yield data


# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from svs_mapper.items import Directory
from scrapy.http import Request, FormRequest
from datetime import date
import hashlib


class EmpresasSpider(scrapy.Spider):
    name = "empresas"
    allowed_domains = ["svs.cl"]
    base_query_url = 'http://www.svs.cl/institucional/mercados/consulta.php?mercado=V&Estado=TO&entidad=%s&_=1441566576260'
    base_url = 'http://www.svs.cl'

    #needed more subtypes
    subtypes_names = {
        'RACRT':'Administradoras de Cartera',
        'RAFIP':'Administradoras de Fondos de Inversión Privados',
        'AGVAL':'Agentes de Valores',
        'BOLPR':'Bolsas de Productos',
        'BOLSA':'Bolsas de Valores',
        'RGCCF':'Caja de Compensación de Asignación Familiar',
        'CLARI':'Clasificadoras de Riesgo',
        'COBOL':'Corredores de Bolsa',
        'IVCBP':'Corredores de Bolsa de Productos',
        'RG268':'Deportivas no profesionales, de beneficencia o educacionales',
        'RVEMI':'Emisores de Valores de Oferta Pública',
        'RGEAE':'Empresas de Auditoria Externa',
        'FINRE':'Fondos de Inversión No Rescatables',
        'RGFEN':'Fondos de Inversión Capital Extranjero (FICE)',
        'RGFER':'Fondos de Inversión Capital Extr. Riesgo',
        'FIRES':'Fondos de Inversión Rescatables',
        'RGFMU':'Fondos Mutuos',
        'RGFVI':'Fondos para la Vivienda',
        'RVSOC':'Otras Sociedades',
        'RGAFP':'Soc. Adm. de Fondos de Pensiones',
        'RGAFI':'Soc. Adm. Fondos Inversión',
        'RGAFC':'Soc. Adm. Fondos Inversión Cap. Extr.',
        'RGAFM':'Soc. Adm. Fondos Mutuos',
        'RGAFV':'Soc. Adm. Fondos para la Vivienda',
        'RGAGF':'Soc. Adm. Generales de Fondos',
        'RGCCO':'Sociedades Adm. de Sistemas de Compensación y Liquidación',
        'RGSEC':'Sociedades Securitizadoras',
        'RVEXT':'Valores Extranjeros'

    }
    today = date.today()
    hesenciales_params = {
        'dd':'01','mm':'01','aa':'2001',
        'dd2':today.strftime("%d"),'mm2':today.strftime("%m"),'aa2':today.strftime("%Y"),
        'dias':'',
        'entidad':'',
        'rut':'' ,
        'formulario':'1'
    }
    sanction_params = {
        'desde':'01/01/2001',
        'rut':'',
        'vig':'',
        'hasta':today.strftime("%d/%m/%Y"),
        'dias':''
    }

    start_urls = [base_query_url % key for key in subtypes_names.keys()]

    def parse(self, response):

        hxs = Selector(response)

        companies = hxs.xpath('//tr[td]')

        for item in companies:
            data = Directory()
            data['company_ICN'] = ''.join(item.xpath('td[1]/a/text()').extract()).strip()
            data['company_name'] = ''.join(item.xpath('td[2]/a/text()').extract()).strip()
            data['company_active'] = ''.join(item.xpath('td[3]/text()').extract()).strip()
            link = self.base_url +'/institucional/mercados/'+ ''.join(item.xpath('td[1]/a/@href').extract()).strip()
            data['reference'] = link

            #essential facts
            request0 = Request(link.replace('pestania=1','pestania=25'),
                              callback = self.hesenciales,
                              meta = {'data':data}
                              )
            yield request0
            request1 = Request(link.replace('pestania=1','pestania=36'),
                              callback = self.sanctions,
                              meta = {'data':data}
                              )

            yield request1

    def sanctions(self, response):

        hxs = Selector(response)

        data = response.meta['data']
        data['type'] = 'Sanction'

        parameters = self.sanction_params

        parameters['rut'] = data['company_ICN'].split('-')[0]
        parameters['vig'] = data['company_active']


        yield FormRequest(
                    url=response.url,
                    meta={'data':data},
                    formdata=parameters,
                    #dont_click=True,
                    callback=self.parse_form)

    def hesenciales(self,response):

        data = response.meta['data']
        data['type'] = 'Essencial'
        #self.log('data: <%s>' % data)
        parameters = self.hesenciales_params
        parameters['rut'] = data['company_ICN'].split('-')[0]
        parameters['entidad'] = data['company_name']
        #parameters['meta'] = data
        #self.log('parameters: <%s>' % parameters)
        yield FormRequest(
                    url=response.url,
                    meta={'data':data},
                    formdata=parameters,
                    #dont_click=True,
                    callback=self.parse_form)

    def parse_form(self,response):

        hxs = Selector(response)
        data = response.meta['data']
        #self.log('body: <%s>' % response.body)

        docs = hxs.xpath('//tr[td]')

        for item in docs:
            #data = Directory()
            data['doc_date'] = ''.join(item.xpath('td[1]/text()').extract()).strip()
            data['doc_ext_id'] = ''.join(item.xpath('td[2]/a/text()').extract()).strip()
            data['doc_url'] = self.base_url + ''.join(item.xpath('td[2]/a/@href').extract()).strip()
            data['doc_desc'] = ''.join(item.xpath('td[4]/text()').extract()).strip()
            #self.log('data: <%s>' % data)
            m = hashlib.md5()
            to_hash = data['type'] + data['company_ICN'] + data['company_name'] + \
                      data['doc_ext_id'] + data['doc_date'] + data['doc_url']
            m.update(to_hash.encode('utf-8'))
            data['id'] = m.hexdigest()
            return data








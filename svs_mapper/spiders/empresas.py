# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from svs_mapper.items import Directory
from scrapy.http import Request, FormRequest
from datetime import date
import hashlib
import time


class EmpresasSpider(scrapy.Spider):
    name = "empresas"
    allowed_domains = ["svs.cl"]
    base_query_url = 'http://www.svs.cl/institucional/mercados/consulta.php?mercado=V&Estado=TO&entidad=%s&_=1441566576260'
    base_query_url_security = 'http://www.svs.cl/institucional/mercados/consulta.php?mercado=S&Estado=TO&entidad=%s&_=1441566576260'
    base_url = 'http://www.svs.cl'

    type= 'Essencial'

    #needed more subtypes
    subtypes_names = {
        'RGABC':'Abogados Calificadores',
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
    subtypes_names_security = {
        'RGAMH':'Agentes Administradores de Mutuos Hipotecarios Endosables',
        'CSCRE':'Cías. de Seguros Crédito',
        'CSVID':'Cías. de Seguros de Vida',
        'CSGEN':'Cías. de Seguros Generales',
        'REEXT':'Cías. Reaseguradoras Extranjeras',
        'RGNAC':'Cías. Reaseguradoras Grales Nacionales',
        'RVNAC':'Cías. Reaseguradoras Vida Nacionales',
        'CREXT':'Corredores de Reaseguros Extranjeros',
        'CRNAC':'Corredores de Reaseguros Nacionales',
        'CSJUR':'Corredores de Seguros - Persona Jurídica',
        'CSNAT':'Corredores de Seguros - Persona Natural',
        'CRVJU':'Corredores Seguros Previs.-pers. jur.',
        'CRVNA':'Corredores Seguros Previs.-pers. nat.',
        'CSEXT':'Corredores y Cías. de Seguros Extranjeros (Por NCG 197)',
        'LSJUR':'Liquidadores de Siniestros - pers. jur.',
        'LSNAT':'Liquidadores de Siniestros - pers. nat.'
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

    start_urls = [base_query_url % key for key in subtypes_names.keys()] + [base_query_url_security % key for key in subtypes_names_security.keys()]

    def __init__(self, type=None,*args, **kwargs):
        super(EmpresasSpider, self).__init__(*args, **kwargs)

        if type is not None:
            self.type = type

    def parse(self, response):

        hxs = Selector(response)

        companies = hxs.xpath('//tr[td]')

        for item in companies:
            data = Directory()
            data['company_ICN'] = ''.join(item.xpath('td[1]/a/text()').extract()).strip()
            data['company_name'] = ''.join(item.xpath('td[2]/a/text()').extract()).strip()
            active = ''.join(item.xpath('td[3]/text()').extract()).strip()
            if (active=='VI') | (active=='NV'):
                data['company_active'] = active
            else:
                data['company_admin'] = active
                data['company_active'] = ''.join(item.xpath('td[4]/text()').extract()).strip()
            link = self.base_url +'/institucional/mercados/'+ ''.join(item.xpath('td[1]/a/@href').extract()).strip()
            data['reference'] = link
            data['scanner_date'] = self.today.strftime('%Y-%m-%dT%H:%M:%SZ')

            #essential facts
            if self.type == 'Essencial':
                request0 = Request(link.replace('pestania=1','pestania=25'),
                                  callback = self.hesenciales,
                                  meta = {'data':data}
                                  )
                yield request0

            elif self.type == 'Sanction':
                request1 = Request(link.replace('pestania=1','pestania=36'),
                                  callback = self.sanctions,
                                  meta = {'data':data}
                                  )

                yield request1
            elif self.type == 'StockHolder':
                request2 = Request(link.replace('pestania=1','pestania=5'),
                                  callback = self.stockholder,
                                  meta = {'data':data}
                                  )
                yield request2

    def stockholder(self,response):
        hxs = Selector(response)

        data = response.meta['data']
        data['type'] = 'StockHolder'
        data['reference'] = response.url

        date_str = ''.join(hxs.xpath('//tr[position() =1]/td[1]/text()').extract()).replace(u'(Ultimo Período Informado)','').strip()
        #06 / 2015
        try:
            date_struct = time.strptime(date_str,'%m / %Y')
            data['stock_date'] = time.strftime('%Y-%m-%dT%H:%M:%SZ',date_struct)
        except:
            self.log('No Information: %s' % response.url)

        stock_list = hxs.xpath('//tr[position() >1]')
        for item in stock_list:
            data['type'] = 'StockHolder'
            data['stock_name'] = ''.join(item.xpath('td[1]/text()').extract()).strip()
            data['stock_percentage'] = ''.join(item.xpath('td[4]/text()').extract()).strip()
            if data['stock_name'] == '':
                data['type'] = 'Company'
            m = hashlib.md5()
            to_hash = data['type'] + data['company_ICN'] + data['company_name'] + \
                      data['stock_name'] + data['stock_percentage']
            m.update(to_hash.encode('utf-8'))
            data['id'] = m.hexdigest()
            yield data


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
            data['doc_ext_id'] = ''
            data['doc_url'] = ''
            if data['type']=='Essencial':
                self.log('type',data['type'])
                date_str = ''.join(item.xpath('td[1]/text()').extract()).strip()
                if (date_str !='') & (date_str !=u'Sin Información'):
                    date_struct = time.strptime(date_str,'%d/%m/%Y %H:%M:%S')
                    data['doc_date'] = time.strftime('%Y-%m-%dT%H:%M:%SZ',date_struct)
                    data['doc_ext_id'] = ''.join(item.xpath('td[2]/a/text()').extract()).strip()
                    data['doc_url'] = self.base_url + ''.join(item.xpath('td[2]/a/@href').extract()).strip()
                    data['doc_desc'] = ''.join(item.xpath('td[4]/text()').extract()).strip()
            else:
                date_str = ''.join(item.xpath('td[2]/text()').extract()).strip()
                if (date_str !='') & (date_str !=u'Sin Información'):
                    date_struct = time.strptime(date_str,'%d.%m.%Y')
                    data['doc_date'] = time.strftime('%Y-%m-%dT%H:%M:%SZ',date_struct)
                data['doc_ext_id'] = ''.join(item.xpath('td[1]/text()').extract()).strip()
                data['doc_url'] = self.base_url + ''.join(item.xpath('td[4]/a/@href').extract()).strip()
                data['doc_desc'] = ''.join(item.xpath('td[3]/text()').extract()).strip()

            if (data['doc_ext_id'] == '') | (data['doc_ext_id'] is None):
                data['type'] = 'Company'
            #self.log('data: <%s>' % data)
            m = hashlib.md5()
            to_hash = data['type'] + data['company_ICN'] + data['company_name'] + \
                      data['doc_ext_id'] + data['doc_url']
            m.update(to_hash.encode('utf-8'))
            data['id'] = m.hexdigest()
            return data








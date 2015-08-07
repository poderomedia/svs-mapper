# -*- coding: utf-8 -*-

# Scrapy settings for svs_mapper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import datetime

BOT_NAME = 'svs_mapper'
LOG_FILE = 'log_'+ str(datetime.date.today())+'.txt'

SPIDER_MODULES = ['svs_mapper.spiders']
NEWSPIDER_MODULE = 'svs_mapper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'svs_mapper (+http://www.yourdomain.com)'

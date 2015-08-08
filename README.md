#SVS Mappers Scraping

This repo contains the project for scrapping data in the SVS site (Chile).
The project was builded using the Scrapy Framework.


## Data Estructure

type: indicates the type of the entity (Boards, Executives, StockHolders, Company)
company_ICN: Company code (Chile - RUT)
company_name: name of the company
person_ICN: Person Code Nmber (Chile - RUT)
person_name: Name of the Person
person_jobtitle: Job title of the Person in the Company
person_jobtitle_desc: Extra data about the Job title position
person_datejob: start date of the person job title
scanner_date: indicates when was obtained that data (running the spider)

## The spiders

There are the following spider:
svs: return all the Boards members
executives: return all the Executives members


## Running a specific spider

Simple execute the following:

``scrapy crawl executives -t csv -o executives.csv``

This command return all executives in csv format in the executives.csv output file.


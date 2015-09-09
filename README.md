#SVS Mappers Scraping

This repo contains the project for scrapping data in the SVS site (Chile).
The project was builded using the python Scrapy Framework.

## The Site

``http://www.svs.cl``
* Contains data from companies regulated by SVS - Chile (Superintendencia de valores y Servicios)

Observation: We have plans for scrapping all the similar sites in SouthAmerica and Caribean Region.
Please send request to add new sites in the issues section.

## Requirements

* python 2.7
* Scrapy Framework 0.24.6

## Installation

If you have Windows, Mac or any Linux, you must follow these instructions.
* Open a terminal window.
* Clone the repo: ``git clone https://github.com/poderomedia/svs-mapper``
* Move to the repo directory: ``cd svs-mapper``
* Install the requirements: ``pip install requirements.txt``

That's all. 

## Data Structure

* id: unique id (hash)
* type: indicates the type of the entity (Boards, Executives, StockHolders, Company, Sanctions)
* company_ICN: Company code (Chile - RUT)
* company_name: name of the company
* company_active: indicates if a company is active or not (values: VIG, NV)
* company_admin: company controller
* person_ICN: Person Code Number (Chile - RUT)
* person_name: Name of the Person
* person_jobtitle: Job title of the Person in the Company
* person_jobtitle_desc: Extra data about the Job title position
* person_datejob: start date of the person job title
* person_datejob_end: end date of the person job title (default is ´-1´ that indicates ´to present´)
* reference: indicates the reference url with the scraped data
* scanner_date: indicates when was obtained that data (running the spider)

### Documents Fields:
* doc_ext_id: External ID of the document
* doc_date: Date of the Document
* doc_desc: Description of the Document
* doc_url: Url of the Document


## The spiders

There are the following spider:
* svs: return all the present Boards members
* executives: return all the present Executives members
* historic_boards: return all the historic Board members (Past and Present)
* sanciones: return all sanctions between two dates (default: 01-01-2001 to present day)
* empresas: return al companies with sanctions and essential facts between two dates (default: 01-01-2001 to present day)


## Running a specific spider

Under the directory of the installed repo, execute the following command:

``scrapy crawl executives -t csv -o executives.csv``

This command return all executives in csv format in the ``executives.csv`` output file.

 In the directory you will see the file ``executives.csv``
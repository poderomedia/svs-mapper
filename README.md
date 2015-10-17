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
* company_market: market of the company (values: Mercado, Seguro)
* company_type: company type
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
* empresas: return all companies with sanctions and essential facts between two dates (default: 01-01-2001 to present day).
Also empresas return the 12 principal stock holders.
 
## Running a specific spider

Under the directory of the installed repo, execute the following command:

``scrapy crawl executives -t csv -o executives.csv``

This command return all executives in csv format in the ``executives.csv`` output file.

In the directory you will see the file ``executives.csv``
 
## Special Case "empresas" spider

The Spider can crawl Esential facts, Sanctions and Stock holders.
To crawl for a specific document you must use the type argument when running the spider.
The type argument can be: "Essencial", "Sanction" or "StockHolder". The default value for type is "Essencial"

For example, to crawl under empresas all the sanctions you must execute in terminal the following command:

``scrapy crawl empresas -a type="Sanction" -t csv -o sanctions.csv``

This command return all Sanctions for all companys in csv format in the ``sanctions.csv`` output file
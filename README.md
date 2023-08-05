# Comicvine-API-scraper-pub
Python script that scrapes Comicvine REST API endpoint to retrive JSON and download to Excel records
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is a small module to hit the GameSpot/Comicvine API and download data from their API endpoint, normalizes/flattens the JSON and returns it via a Python Pandas dataframe.
	
## Technologies

Project was developed with:
* Python version 3.9.0
These library depedencies must be installed in your environment
* requests 
* json 
* sys
* os
* datetime
* time
* random
* xlsxwriter
* pandas
* datetime
* random
* time
* sys

## Files
* ComicvineAPIScrape.py (the class module)
* ComicvineAPI-scrape-client-code.py (example client code for help)

## Setup
```
Pre-requisite:
You must register for an API at gamespot/comicvine at https://comicvine.gamespot.com/api/
Insert your API key into your object instatiation code as displayed in the example ComicvineAPI-scrape-client-code.py: 
	ComicvineAPIScrape.ComicvineAPI_scraper('C:\\Users\\00616891\\Downloads\\CV_API_output\\', '<API key>','issues', 400)
```
```
For needed Pythong packages, See Technologies section...

To run this project, install ComicvineAPIScrape.py in <project location>\Lib\site-packages

Notable method and property/attribute calls:
    scraper = ComicvineAPIScrape.ComicvineAPI_scraper('C:\\Users\\00616891\\Downloads\\CV_API_output\\', '<API key>','issues', 400)
	
	print("attributes_CV_resp code in client code: {}".format(scraper.attributes_CV_resp["response_code"]))
	
	scraper.attributes_CV_resp["response_code"] 
	
	df_result = scraper.df_CV #this is a return of the API (JSON data) in Pandas Datframe form
```



# -*- coding: utf-8 -*-
#Created on Mon Jan 17 22:40:38 2022
#Kevin Faterkowski

import pandas as pd
import requests 
import json 
import sys
import os #for file path testing
import datetime
import time
#from XlsxWriter import FileCreateError
import random
#NOTE: there is a dependency within pandas that may require xlsxwriter in order to write DataFrame to Excel, so include it
import xlsxwriter 

#############################################################################################
#PURPOSE:  is to retrive JSON from a ComicVine REST API endpoint and download to Excel records
#CREDIT TO: https://josephephillips.com/blog/how-to-use-comic-vine-api-part1
#REFERENCE: #https://comicvine.gamespot.com/api/
#01/07/2022 - initial script creation
#01/22/2023 - "globalized" constants in process of converting to a Class...
#############################################################################################
#Constants to populate before execution:
#############################################################################################
##"path_output" - local or network folder/share to store outputs (inc'l log file)
## "CV_API_KEY" - sign up for comicvine API and paste in your API key
#############################################################################################

#############################################################################################

class ComicvineAPI_scraper:
#Class variables:
    base_endpt = "http://comicvine.gamespot.com/api/"
    #you must include this headers parameters because the comicvine API requires a "unique user agent" - cannot be null
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    APIlog_file = "API_log.txt"
    #this is the preventative "stop" between comicvine API calls
    CV_wait_time = 22
    
    def __init__(self
                ,path_output
                ,CV_API_KEY
                ,CV_resource
                ,CV_offset
                ):
        self.path_output = path_output
        self.CV_API_KEY = CV_API_KEY
        self.CV_resource = CV_resource
        self.CV_offset = CV_offset  #NOTE: this attribute DOES NOT have its own setter, getter - interesting option
        self.CV_query_string = "/?api_key="
        self.resp_format = "&format=json"
        self.CV_query_URL = None
        #this is the dataFrame that will be exposed to the client code for easy retreival
        self.df_CV = None
        #private attributes:         #Prefixing with '_' indicates it's a private attribute
        self.CV_timestamp = None #set to the current time of obj. construction
        #dict to hold response code and response JSON
        self.attributes_CV_resp = {}

    #end of __init__
    
    @property 
    def path_output(self):
    #NOTE: you must put an underscore before the instance variable name or else the "getter" will act as a recursive call, throwing a limit error
        return self._path_output
    
    @path_output.setter
    def path_output(self, path_output):
    #this type of setter will always be called upon calling __init__()
        if not os.path.exists(path_output):
            raise Exception("the output path provided is invalid, destroying the object")
        self._path_output = path_output

    #https://towardsdatascience.com/6-approaches-to-validate-class-attributes-in-python-b51cffb8c4ea
    @property 
    def CV_API_KEY(self):
        return self._CV_API_KEY
    
    @CV_API_KEY.setter 
    def CV_API_KEY(self, CV_API_KEY):
        #only validation is key length
        if( len(CV_API_KEY) < 40):
            raise Exception("API Key is insufficient length, destroying object")
        self._CV_API_KEY = CV_API_KEY
        
    @property 
    def CV_resource(self):
        return self._CV_resource
    
    @CV_resource.setter 
    def CV_resource(self, CV_resource):
        valid_resource = (
            'issues'
            ,'characters'
            )
        #validation
        if CV_resource not in valid_resource:
            raise Exception("CV_resource parameter provided is invalid, destroying the object")
        self._CV_resource = CV_resource
        
    @property 
    def CV_offset(self):
        return self._CV_offset
    
    @CV_offset.setter 
    def CV_offset(self, CV_offset):
        #validation
        if type(CV_offset) is not int: 
            raise Exception("CV_offset parameter provided is invalid, destroying the object")
        #NOTE: you must put an underscore before the instance variable name or else the "getter" will act as a recursive call, throwing a limit error
        self._CV_offset = CV_offset
    
    @property 
    def CV_query_URL(self):        
        return self._CV_query_URL
    
    @CV_query_URL.setter
    def CV_query_URL(self, CV_offset):
        #NOTE: you must put an underscore before the instance variable name or else the "getter" will act as a recursive call, throwing a limit error
        self._CV_query_URL = self.build_query_string()
    
    #not using a property decorator since I do not want to have a getter/setter pair for this "private"
    #https://stackoverflow.com/questions/27396339/attributeerror-cant-set-attribute
    def get_CV_timestamp(self):
        return self.CV_timestamp
       
    #Using properties: You can use the @property decorator to define a getter method 
    #but omit the setter method for a READ-ONLY attribute,  
    #attempting to modify it will result in an "AttributeError: can't set attribute"
    #thus, you should only do this when you intend to create a read-only attribute with NO setting 
    def df_CV(self):        
        return self.df_CV
    
    #not using a property decorator since I do not want to have a getter/setter pair for this "private"
    def attributes_CV_resp(self):
        return self.attributes_CV_resp

#end of class inits
# =============================================================================

    def execute_get(self):
        #this function actually executes the API call, get()
        
        with open(self.path_output + self.APIlog_file, "a") as logfile:

            try:
                print("execute_get() at {}".format(datetime.datetime.now())) 
                
                #build the query string (a "private" variable)
                self.build_query_string()
                
                CV_resp = requests.get(self._CV_query_URL, headers = self.headers)
                    
                #a response of 200 is OK
                print("GET response at {}: {}".format(datetime.datetime.now(), CV_resp))
                
                self.attributes_CV_resp["response_code"] = CV_resp.status_code #populate dict
                
                if CV_resp.status_code == 200: #test for succesful response
    
                #NOTE: you must use the .json() or json.dumps() methods to ensure the object is serializable
                    
                    self.attributes_CV_resp["response_JSON"] = json.dumps(CV_resp.json(), indent=4) #populate dict
                     
                    # if not CV_resp:
                    #     print("no more results from API call.")
                    #     logfile.write(str(datetime.datetime.now()) + " no more results from API call.\n")
                    #     sys.exit()
                            
                else: 
                     print("bad response, write to log file...")
    
            except requests.Timeout as e:
                print("a Timeout error occured: {} \n".format(e))
            except requests.ConnectionError as e:
                print("a ConnectionError error occured: {} \n".format(e))
            except requests.InvalidURL as e:
                print("a InvalidURL error occured: {} \n".format(e))
    #end of method execute_get()
    
    def make_request(self):
    #this function is a governor to ensure we don't spam the REST endpoint and get banned
   

        with open(self.path_output + self.APIlog_file, "a") as logfile:    

            try:             
                #if(self._CV_timestamp is not None): #this is the first get() request for the object instance
                if(self.CV_timestamp is not None): #this is the first get() request for the object instance
                
                    #you have to do some kind of modulo for timedelta
                    time_to_wait = datetime.datetime.now() - self.CV_timestamp
                    
                    if(time_to_wait / datetime.timedelta(seconds=1) < self.CV_wait_time):  #you are only allowed 200 Comicvine calls per hour per resource
                        print("Too early to execute a get(): time since last GET() is {}, current time is {}".format( time_to_wait / datetime.timedelta(seconds=1),datetime.datetime.now() ) )
                        return
                
                self.CV_timestamp = datetime.datetime.now()
                self.execute_get() #tore the timestamp to the instance attribute
                
                if (self.attributes_CV_resp["response_code"]  == 200 ):
                    logfile.write("{} JSON was successfully retrieved from endpoint...\n".format(datetime.datetime.now()))
                    self.process_JSON()                
                    self.timestamp_df()
                
                else: 
                    "non-200 API response, continuing..."
                
            except requests.Timeout as e:
                print("a Timeout error occured: {} \n".format(e))
            except requests.ConnectionError as e:
                print("a ConnectionError error occured: {} \n".format(e))
            except requests.InvalidURL as e:
                print("a InvalidURL error occured: {} \n".format(e))
        #end of make_request()   

    def process_JSON(self):
    # there was a valid response, so normalize the temporary JSON        
        try: 

            # You use json.loads to convert a JSON string into Python objects needed  to read nested columns
            # also we are creating a DataFrame from the normalized JSON
            #https://stackoverflow.com/questions/68864871/why-does-pandas-json-normalizejson-results-raise-a-notimplementederror
            
            self.df_CV = pd.json_normalize(json.loads( self.attributes_CV_resp["response_JSON"] ), record_path =['results'],meta=['error', 'limit', 'offset'])
            
            #write the temporary JSON for now - just for debugging purposes
            with open(self.path_output + "temp_json.json", "w") as file_json:
                file_json.write( self.attributes_CV_resp["response_JSON"] )
            
            print("dataframe in process_json(): /n", self.df_CV.shape)
            
        except Exception as e:
            print("general exception in process_JSON(): {} \n".format(e))
        except pd.NotImplementedError as nie:
            print("notimplementederror in timestampt_df(): {} \n".format(nie))
    #end of process_JSON()

    def timestamp_df(self):
        
        try:
         
            #grab the current date for timestamping
            formatted_date = datetime.datetime.now()
            formatted_date = formatted_date.strftime('%M-%D-%Y')
            
            #append the timestamp column onto the dataframe     
            self.df_CV['TS_pulled'] = formatted_date
    
        except Exception as e:
            print("general exception in timestamp_df(): {} \n".format(e))

    #end of timestamp_df()
    
    
    def build_query_string( self ):
        
        CV_filter_string = ""
        
        #https://comicvine.gamespot.com/forums/api-developers-2334/paging-through-results-page-or-offset-1450438/
        #The end of the "characters" resource list is around 149150
        CV_sort_offset_string = "&sort=name: asc&offset=%s"%(self.CV_offset)
        self._CV_query_URL = self.base_endpt + self.CV_resource + self.CV_query_string + self.CV_API_KEY + CV_filter_string + CV_sort_offset_string + self.resp_format
    
    #end of build_query_string()

#end of class ComicvineAPI_scraper
#################################################################################################################
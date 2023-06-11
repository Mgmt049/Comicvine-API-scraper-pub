# -*- coding: utf-8 -*-
#Created on Mon Jan 17 22:40:38 2022
#Kevin Faterkowski

import pandas as pd
import requests 
import json 
import sys
import os #for file path testing
import datetime
import shutil as sh
import time
#from XlsxWriter import FileCreateError

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
        #privates:
        self._CV_timestamp = None #set to the current time of obj. construction
        #self._CV_offset = None
        self._CV_processed_json = None

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
#            del(self)
        self._path_output = path_output

    #https://towardsdatascience.com/6-approaches-to-validate-class-attributes-in-python-b51cffb8c4ea
    @property 
    def CV_API_KEY(self):
        return self._CV_API_KEY
    
    @CV_API_KEY.setter 
    def CV_API_KEY(self, CV_API_KEY):
        #=======
        #ACTION: put in a validation
        self._CV_API_KEY = CV_API_KEY
        
    @property 
    def CV_resource(self):
        #NOTE: add some validation
        return self._CV_resource
    
    @CV_resource.setter 
    def CV_resource(self, CV_resource):
        valid_resource = (
            'issues'
            ,'characters'
            )
        #validation
        if CV_resource not in valid_resource:
            raise Exception("resource parameter provided is invalid, destroying the object")
        self._CV_resource = CV_resource
    
    @property 
    def CV_query_URL(self):        
        return self._CV_query_URL
    
    @CV_query_URL.setter
    def CV_query_URL(self, CV_offset):
        #NOTE: add some validation for offset
        #NOTE: you must put an underscore before the instance variable name or else the "getter" will act as a recursive call, throwing a limit error
        self._CV_query_URL = self.build_query_string()
        #self._CV_query_URL = self.build_query_string()
    
    #not using a property decorator since I do not want to have a getter/setter pair for this "private"
    #https://stackoverflow.com/questions/27396339/attributeerror-cant-set-attribute
    def get_CV_timestamp(self):
        return self._CV_timestamp
    
    #not using a property decorator since I do not want to have a getter/setter pair for this "private"
    #https://stackoverflow.com/questions/27396339/attributeerror-cant-set-attribute
    def get_processed_json(self):
        return self._CV_processed_json
    
# =============================================================================
# def load_previous(dir_output):
#     #to mark when previous dataset is loaded:
#     ts_start = datetime.datetime.now()
#     print("timestamp pulled in load_previous:", ts_start)
#     
#     dir_output = dir_output+'Comicvine.xlsx'
#     
#     #setup the error log:
#     with open(GLOBALS["path_output"]+GLOBALS["APIlog_file"], mode="a") as err_file:
#         try:
# 
#             #you must specify index_col=0 to prevent new indexes from being created
#             full_data = pd.read_excel(dir_output, index_col=0)
#             print("dataframe shape in load_previous: ", full_data.shape)
#             ts_postload = datetime.datetime.now()
# 
#             print("it took this long? {}\n".format(ts_postload - ts_start))
#             
#             #return a dataframe    
#             return full_data
#         
#         except FileNotFoundError as e:
#             print("this the FNF error", e)
#             err_file.write("{} this the FNF error {} \n".format(datetime.datetime.now(), e) )
#             sys.exit() #terminate the whole program
#         except IOError as io:
#             print("this the IO error: ", io)
#             #err_file.write("this the IO error", datetime.datetime.now())
#             err_file.write("{} this the IO error {} \n".format(datetime.datetime.now(), io) )
#             sys.exit() #terminate the whole program
# 
# 
    def build_query_string( self ):
        
        CV_filter_string = ""
        
        #https://comicvine.gamespot.com/forums/api-developers-2334/paging-through-results-page-or-offset-1450438/
        #The end of the "characters" resource list is around 149150
        CV_sort_offset_string = "&sort=name: asc&offset=%s"%(self.CV_offset)
        
        #return self.base_endpt + self.CV_resource + self.CV_query_string + self.CV_API_KEY + CV_filter_string + CV_sort_offset_string + self.resp_format
        self._CV_query_URL = self.base_endpt + self.CV_resource + self.CV_query_string + self.CV_API_KEY + CV_filter_string + CV_sort_offset_string + self.resp_format
    

    def normalize_df(self):
     
        #grab the current date for timestamping
        formatted_date = datetime.datetime.now()
        formatted_date = formatted_date.strftime('%M-%D-%Y')
        print("timestamp pulled in normalize_df() %s"%(datetime.datetime.now()))
        
        #json_CV = pd.json_normalize(json_CV, record_path =['results'],meta=['error', 'limit', 'offset'])
        #self._CV_processed_json is the finalized JSON result from the API call and processing
        df_json_CV = pd.json_normalize(self._CV_processed_json, record_path =['results'],meta=['error', 'limit', 'offset'])
        #append the timestamp column onto the dataframe
        #json_CV['TS_pulled'] = datetime.datetime.now()
        df_json_CV['TS_pulled'] = datetime.datetime.now()
        #return json_CV
        return df_json_CV
    
    #end of normalize_df()

# def calc_offset(df):
#     #The end of the "characters" resource list is ~149150
#     #use len() to return number of rows
#     return ( len(df) + 1 )

    def execute_get(self):
        
        with open(self.path_output + self.APIlog_file, "a") as logfile:

            try:
                print("execute_get() at {}".format(datetime.datetime.now())) 
                
                #self.CV_query_string = self.build_query_string()
                
                #build the query string (a "private" variable)
                self.build_query_string()
                
                print("full query string/endpoint: {}".format(self._CV_query_URL))
                
                #CV_resp = requests.get(self.full_endpt, headers = self.headers)
                CV_resp = requests.get(self._CV_query_URL, headers = self.headers)
                    
                #a response of 200 is OK
                print("GET response at {}: {}".format(datetime.datetime.now(), CV_resp))
                
                if CV_resp.status_code == 200: #test for succesful response
    
                #NOTE: you must use the .json() or json.dumps() methods to ensure the object is serializable
                    obj_json = json.dumps(CV_resp.json(), indent=4)
                     
                    if not CV_resp:
                        print("no more results from API call.")
                        logfile.write(str(datetime.datetime.now()) + " no more results from API call.\n")
                        sys.exit()
                
                #ACTION: CALL THE process_JSON METHOD HERE
                    self._CV_processed_json = self.process_JSON(obj_json)
                    logfile.write("{} JSON was successfully retrieved from endpt...\n".format(datetime.datetime.now()))
                     
                    #return json_processed #return a json object
                            
                else: 
                     print("bad response, write to log file...")
    
            except requests.Timeout as e:
                print("a Timeout error occured: {} \n".format(e))
            except requests.ConnectionError as e:
                print("a ConnectionError error occured: {} \n".format(e))
            except requests.InvalidURL as e:
                print("a InvalidURL error occured: {} \n".format(e))
    #end of method execute_get()
    
    def process_JSON(self, obj_json):
        #this method is to do a JSON "swap" that is necessary for usable JSON
        print("process_JSON() called")
        #there was a valid response, so handle the temporary JSON - do a WRITE and then an immediate READ
        with open(self.path_output + "temp_json.json", "w") as file_json:
            file_json.write(obj_json)
        #You use json.loads to convert a JSON string into Python objects needed  to read nested columns
        with open(self.path_output + "temp_json.json",'r') as file_json:
            json_formatted = json.loads(file_json.read())
            return json_formatted #return a json object
    #end of process_JSON()

    #def make_request(full_endpt, headers, offset):
    def make_request(self):
    #this function is a governor to ensure we don't spam the REST endpoint and get banned
   
     #ACTION: WRITE EXCEPTIONS TO LOGFILE IN THE ELSE CONDITIONS AND THE EXCEPTS!!!!!    
        with open(self.path_output + self.APIlog_file, "a") as logfile:    

            try:             
                if(self._CV_timestamp is not None): #this is the first get() request for the object instance       
                    #you have to do some kind of modulo for timedelta???
                    time_to_wait = datetime.datetime.now() - self._CV_timestamp
                    if(time_to_wait / datetime.timedelta(seconds=1) < 80):  #keep the throttle at 1 minute 20 seconds just in case
                        print("cannot get() YET! - time since last GET() is {}, current time is {}".format( time_to_wait / datetime.timedelta(seconds=1),datetime.datetime.now() ) )
                        return
                
                #ACTION: figure out the offset problem and then do a git commit
                #store the timestamp for banning safety and commence the actual get()               
                self._CV_timestamp = datetime.datetime.now()
                self.execute_get()
                df_API_result = self.normalize_df()
                return df_API_result
                
            except requests.Timeout as e:
                print("a Timeout error occured: {} \n".format(e))
            except requests.ConnectionError as e:
                print("a ConnectionError error occured: {} \n".format(e))
            except requests.InvalidURL as e:
                print("a InvalidURL error occured: {} \n".format(e))
        #end of make_request()   


# def combine_dfs(dfs):
#     #concat must be passed an "iterable"/"array" of Dataframe objects, I believe ignore_index is
#     #necessary for re-numbering the index
#     return pd.concat(dfs, axis=0, ignore_index=True)
# 
# def write_results(df_full_data, path_output):
#     #setup the error log:
#     with open(GLOBALS["APIlog_file"], mode="a") as err_file:
# 
#         path_output = path_output + "Comicvine.xlsx"        
# 
#         try:
#             
#             #quickly create a backup file
#             sh.copy2(path_output, 'C:\\Users\\00616891\\Downloads\\CV_API_output\\Comicvine_bak.xlsx')
#             
#             #df_full_data.to_excel(path_output)
#     
#             #Excel threw a hard limit on 65K+ URLS error, so i had to use Excelwriter() and ingore URLs instead of .toExcel()
#             #https://pandas.pydata.org/docs/reference/api/pandas.ExcelWriter.html
#             #https://stackoverflow.com/questions/55280131/no-module-named-xlsxwriter-error-while-writing-pandas-df-to-excel/55280686
#             #https://stackoverflow.com/questions/71144242/which-arguments-is-futurewarning-use-of-kwargs-is-deprecated-use-engine-kwa
#             with pd.ExcelWriter(path_output, engine='xlsxwriter', engine_kwargs={'options':{'strings_to_urls': False}}) as writer:
#                 df_full_data.to_excel(writer)
#             
#             print("timestamp pulled in write_results() %s"%(datetime.datetime.now()))
# 
#         except FileNotFoundError as e:
#             print("this the FNF error", e)
#             err_file.write("{} this the FNF error {} ".format(datetime.datetime.now(), e) )
#             sys.exit() #terminate the whole program
#         except IOError as io:
#             print("this the IO error: ", io)
#             err_file.write("{} this the IO error {} ".format(datetime.datetime.now(), io) )
#             sys.exit() #terminate the whole program 

def main():
    
    scraper = ComicvineAPI_scraper('C:\\Users\\00616891\\Downloads\\CV_API_output\\', 'f4c0a0d5001a93f785b68a8be6ef86f9831d4b5b', 'issues', 400)
    print(scraper.path_output)    
    print(scraper.CV_query_URL)

    for i in range(1,50):

        df_result = scraper.make_request()
        #print(scraper.get_processed_json())
        if(df_result is not None):
            #print( df_result.head() )
            #display a slice of the dataFrame
            print( df_result.iloc[0:5,3:7] )
        print("start to sleep at: {}".format(datetime.datetime.now()))
        time.sleep(3)  #paramter is in SECONDS    

    #for i in range (0,10):    
                
        #return a dataFrame of the previously-pulled entries
        #df_full_data = load_previous(GLOBALS["path_output"])
        
        #retrieve offset for query string as an integer
        #offset = calc_offset(df_full_data)   
        
        #pass an integer and retrieve a full http query string
        #full_endpt = build_query_string(GLOBALS["base_endpt"], offset)
        
        #print(full_endpt)
        
        #request JSON
        #json_CV = make_request(full_endpt, GLOBALS["headers"], offset)
        
        # Normalizing data - creates a dataFrame
        #f_CV_norm = normalize_df(json_CV)
        
        #df_full_data = combine_dfs([df_full_data,df_CV_norm]) #pass a list of dataframes: "old" and new
            
        #print("df_full_data in main(): ", df_full_data.shape)
        
        #write combined results to file
        #write_results(df_full_data, GLOBALS["path_output"])
        
        #time.sleep(600)
        
if __name__ == "__main__":
    main()

# =============================================================================

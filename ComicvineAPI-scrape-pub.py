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

#ACTION: DO THIS https://towardsdatascience.com/6-approaches-to-validate-class-attributes-in-python-b51cffb8c4ea
GLOBALS = {#"path_output":'C:\\Users\\00616891\\Downloads\\CV_API_output\\',
           "CV_API_KEY" : "f4c0a0d5001a93f785b68a8be6ef86f9831d4b5b", #do not use quotes around the key!
           #you must include this headers parameters because the comicvine API requires a "unique user agent" - cannot be null
           "headers":{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"},
           "base_endpt":"http://comicvine.gamespot.com/api/",
           #"CV_resource" : "characters",
           "CV_resource" : "issues",
           "APIlog_file": "API_log.txt"
           }
#############################################################################################

class ComicvineAPI_scraper:
    def __init__(self
                ,path_output):
        
        if os.path.exists(path_output):
            self.path_output = path_output
        else:
            raise Exception("the output path provided is invalid, destroying object")
            del(self)
        
    #end of __init__
    
    @property
    def get_path_output(self):
    #get the path for the archive folder to be stored:
        return self.path_output
    #end get_path_output
    
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
# def build_query_string(base_endpt, offset):
#     
#     #CV_resource = "characters"
#     CV_query_string = "/?api_key="
#     CV_filter_string = ""
#     
#     #https://comicvine.gamespot.com/forums/api-developers-2334/paging-through-results-page-or-offset-1450438/
#     #The end of the "characters" resource list is around 149150
#     CV_sort_offset_string = "&sort=name: asc&offset=%s"%(offset)
#     
#     resp_format = "&format=json"
#     #return base_endpt + CV_resource + CV_query_string + CV_API_KEY + CV_filter_string + CV_sort_offset_string + resp_format
#     return base_endpt + GLOBALS["CV_resource"] + CV_query_string + GLOBALS["CV_API_KEY"] + CV_filter_string + CV_sort_offset_string + resp_format
# 
# def normalize_df(json_CV):
#     
#     #grab the current date for timestamping
#     formatted_date = datetime.datetime.now()
#     formatted_date = formatted_date.strftime('%M-%D-%Y')
#     print("timestamp pulled in normalize_df() %s"%(datetime.datetime.now()))
#     
#     json_CV = pd.json_normalize(json_CV, record_path =['results'],meta=['error', 'limit', 'offset'])
#     #append the timestamp column onto the dataframe
#     json_CV['TS_pulled'] = datetime.datetime.now()
#     return json_CV
# 
# def calc_offset(df):
#     #The end of the "characters" resource list is ~149150
#     #use len() to return number of rows
#     return ( len(df) + 1 )
# 
# def make_request(full_endpt, headers, offset):
#     
#     #ACTION: WRITE EXCEPTIONS TO LOGFILE IN THE ELSE CONDITIONS AND THE EXCEPTS!!!!!
#     with open(GLOBALS["path_output"]+GLOBALS["APIlog_file"], "a") as logfile:
#         
#         try:
#             resp_CV = requests.get(full_endpt, headers = headers)
#             
#             #a response of 200 is OK
#             print("response at {}: {}".format(datetime.datetime.now(), resp_CV))
#             
#             if resp_CV.status_code == 200: #test for succesful response
#             
#     
#                 #NOTE: you must use the .json() or json.dumps() methods to ensure the object is serializable
#                     obj_json = json.dumps(resp_CV.json(), indent=4)
#                     
#                     #print("type of json object?: ", resp_CV.json().length)
#                     
#                     if not resp_CV:
#                         print("no more results from API call.")
#                         logfile.write(str(datetime.datetime.now()) + " no more results from API call.\n")
#                         sys.exit()
#                     
#                     #there was a valid response, so handle the temporary JSON...
#                     with open(GLOBALS["path_output"]+"temp_json.json", "w") as file_json:
#                         file_json.write(obj_json)
#                     #You use json.loads to convert a JSON string into Python objects needed  to read nested columns
#                     with open(GLOBALS["path_output"]+"temp_json.json",'r') as file_json:
#                         json_CV = json.loads(file_json.read())
#                     
#                     logfile.write("{} JSON was successfully retrieved from endpt...\n".format(datetime.datetime.now()))
#                     return json_CV #return a json object
#                         
#             else: 
#                 print("bad response, write to log file...")
#                 
#         except requests.Timeout as e:
#             print("a Timeout error occured: {} \n".format(e))
#         except requests.ConnectionError as e:
#             print("a ConnectionError error occured: {} \n".format(e))
#         except requests.InvalidURL as e:
#             print("a InvalidURL error occured: {} \n".format(e))
# 
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
    
    scraper = ComicvineAPI_scraper('C:\\Users\\00616891\\Downloads\\CV_API_output\\')
    print(scraper.get_path_output)

    #for i in range (0,10):    
        
        #you must include this headers parameters because the comicvine API requires a "unique user agent" - cannot be null
        #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        
        #return a dataFrame
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

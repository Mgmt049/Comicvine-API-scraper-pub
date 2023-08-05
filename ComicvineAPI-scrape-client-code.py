# -*- coding: utf-8 -*-
#Created on Mon Jan 17 22:40:38 2022
#Kevin Faterkowski

#import ComicvineAPI_scraper
import ComicvineAPIScrape
import random
import pandas as pd
import datetime 
import time
import sys
#################################################################################################################
#start of client code:    
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
# def calc_offset(df):
#     #The end of the "characters" resource list is ~149150
#     #use len() to return number of rows
#     return ( len(df) + 1 )
#
# def combine_dfs(dfs):
#     #concat must be passed an "iterable"/"array" of Dataframe objects, I believe ignore_index is
#     #necessary for re-numbering the index
#     return pd.concat(dfs, axis=0, ignore_index=True)
# 
def write_results(df_full_data, path_output):
    #setup the error log:
    with open(path_output + "APIlog_file", mode="a") as err_file:

        path_output = path_output + "Comicvine_class.xlsx"        

        try:
            
            #quickly create a backup file
            #sh.copy2(path_output, 'C:\\Users\\00616891\\Downloads\\CV_API_output\\Comicvine_bak.xlsx')
    
            #Excel threw a hard limit on 65K+ URLS error, so i had to use Excelwriter() and ingore URLs instead of .toExcel()
            #https://pandas.pydata.org/docs/reference/api/pandas.ExcelWriter.html
            #https://stackoverflow.com/questions/55280131/no-module-named-xlsxwriter-error-while-writing-pandas-df-to-excel/55280686
            #https://stackoverflow.com/questions/71144242/which-arguments-is-futurewarning-use-of-kwargs-is-deprecated-use-engine-kwa
            with pd.ExcelWriter(path_output, engine='xlsxwriter', engine_kwargs={'options':{'strings_to_urls': False}}) as writer:
                df_full_data.to_excel(writer)
            
            print("timestamp pulled in write_results() %s"%(datetime.datetime.now()))

        except FileNotFoundError as e:
            print("this the FNF error", e)
            err_file.write("{} this the FNF error {} ".format(datetime.datetime.now(), e) )
            sys.exit() #terminate the whole program
        except IOError as io:
            print("this the IO error: ", io)
            err_file.write("{} this the IO error {} ".format(datetime.datetime.now(), io) )
            sys.exit() #terminate the whole program 

    
def main():
    
    #ACTION: clean up the module name and the class name (redundant)
    scraper = ComicvineAPIScrape.ComicvineAPI_scraper('C:\\Users\\00616891\\Downloads\\CV_API_output\\', '<API key>','issues', 400)
    
    #loop through 100 API calls and then report out the return code and pull the responses' data via Pandas dataframe
    for i in range(1, 100):
    
        offset = random.randint(1, 100000)
        
        scraper.CV_offset = offset
        
        #initiate a get() to the API 
        scraper.make_request()
        #print(scraper.CV_query_URL)
        
        print("attributes_CV_resp code in client code: {}".format(scraper.attributes_CV_resp["response_code"]))
        
        df_result = scraper.df_CV #this is a return of the API (JSON data) in Pandas Datframe form
           
        if(scraper.attributes_CV_resp["response_code"] == 200):       
            write_results(df_result, 'C:\\Users\\00616891\\Downloads\\CV_API_output\\')         
            
            print("shape of dataframe: {}".format(df_result.shape))           
            print(df_result.iloc[0:10,4:10])
            #print(df_result['volume.name'][3:10])
            print("sleep at: {}".format(datetime.datetime.now()))
            time.sleep(3)  #parameter is in SECONDS    
        
if __name__ == "__main__":
    main()

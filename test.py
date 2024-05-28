import requests
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from requests.exceptions import ProxyError, ReadTimeout, ConnectTimeout
import string

def dateChanger(dateInStr):

    if(dateInStr[3] == " "):
        dd = dateInStr[0:1]
        mm = dateInStr[3:-5]
        yyyy = dateInStr[-4:]
        
    else:
        dd = dateInStr[0:2]
        mm = dateInStr[5:-5]
        yyyy = dateInStr[-4:]

    print(mm.lower().strip())
    if(mm.lower() == "january"):
        mm='01'
    elif(mm.lower() == "february"):
         mm='02'
    elif(mm.lower() == " march"):
         mm='03'
    elif(mm.lower() == " april"): 
         mm='04'
    elif(mm.lower() == "may"):
         mm='05'
    elif(mm.lower() == "june"):
         mm='06'
    elif(mm.lower() == "july"):
         mm='07'
    elif(mm.lower() == "august"):
         mm='08'
    elif(mm.lower() == "september"):
         mm='09'
    elif(mm.lower() == "october"):
         mm='10'
    elif(mm.lower() == "november"):
         mm='11'
    else:
        mm='12'
    print (dd+"/"+mm+"/"+yyyy)






dateChanger("23rd August 2024")
dateChanger("1st July 2024")
dateChanger("20th September 2024")

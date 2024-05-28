import requests
import re
from datetime import date
from bs4 import BeautifulSoup 
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

response = requests.get('https://www.unihomes.co.uk/property/1412023209/birmingham/harborne/5-bedroom-student-house/hilldrop-grove',headers=headers)

soup = BeautifulSoup(response.text, "html.parser")
scriptTags = soup.find_all('script')
# Find all script tags 
print('length---->', len(scriptTags) )
print(scriptTags)
for script in scriptTags:   
    # results = re.search("var property = ", script.text)
    # print('results-----',results)
    # if results:
    #     print('search:-----', results[0])
    
    # OR
     results = re.findall("location '(.*)'", script.text)
     if results:
         print('findall:', results[0])   


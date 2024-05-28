import requests
import json
import psycopg2
from bs4 import BeautifulSoup
from psycopg2.extras import RealDictCursor
from requests.exceptions import ProxyError, ReadTimeout, ConnectTimeout
#CHANGE
conn = psycopg2.connect(database = "UniHomes", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "admin",
                        port = 5432)

TIMEOUT_IN_SECONDS = 10
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def startCrawler():
    #PROXY = '108.165.187.161:13308'
    # proxyMap = {
    #     'http': PROXY
    # }
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM citydetails;') #CHANGE
    #cur.execute('SELECT * FROM testcitydetails;')
    Cities = cur.fetchall()

    cur.execute('SELECT * FROM proxydetail;')#CHANGE
    ProxyList = cur.fetchall()
    proxyMap={}

    for i in range(0,len(ProxyList)):
        proxyMap[i]=ProxyList[i]["proxy"]#CHANGE

    for City in Cities:
            cityName = (City['urlextension'])#CHANGE
            print(cityName)
            try:
                response = requests.get('https://www.unihomes.co.uk/student-accommodation/'+cityName+'?page=1&reload=true', headers=headers,proxies=proxyMap, timeout=TIMEOUT_IN_SECONDS)
            except (ProxyError, ReadTimeout, ConnectTimeout) as error:
                    print('Unable to connect to the proxy: ', error)
            else:
                f = open("jsonfilewrite.txt", "w")
                f.write(str(response.content.decode()))
                f = open('jsonfilewrite.txt')
                data = json.load(f)
                for i in data['properties']:
                    id = i['id']
                    path = i['path']
                    r = requests.get(path)
                    bs = BeautifulSoup.BeautifulSoup(r.text, "html.parser")
                    scripts = bs.find_all('script')
                    jsonObj = None
                    ##CHANGE
                    #insertString = "INSERT INTO public.propertydetails(id, availablefrom, bathroomcount, images_url, landlordname, path, postcode, rentpcm, processed, toolkitid, sourcename)VALUES ("+str(id)+",'"+availableFrom+"', "+str(bathroomcount)+", '"+imagefileURLTablet+"', '"+Landlordname+"', '"+path+"', '"+str(postCode)+"',"+str(rentpcm)+"," + str(processed)+",'"+toolkidID+"','"+sourceName+"')"
                    ##print(insertString)
                    #cur.execute(insertString)
                propertCount = data['propertyCount']
                if(propertCount > 18 ):
                    numberOfPages = round(propertCount/18)
                else:
                    numberOfPages = 1

                if(numberOfPages > 1) : 
                    for pageNumber in range(2,numberOfPages) :
                        try:
                            response = requests.get('https://www.unihomes.co.uk/student-accommodation/'+cityName+'?page='+str(pageNumber)+'&reload=true', headers=headers,proxies=proxyMap, timeout=TIMEOUT_IN_SECONDS)
                        except (ProxyError, ReadTimeout, ConnectTimeout) as error:
                            print('Unable to connect to the proxy SERVER: ', error)
                        else:
                            f = open("jsonfilewrite.txt", "w")
                            f.write(str(response.content.decode()))
                            f = open('jsonfilewrite.txt')
                            data = json.load(f)
                            for i in data['properties']:                               
                                id = i['id']
                                path = i['path']

                                ##CHANGE
                                #insert = "INSERT INTO public.propertydetails(id, availablefrom, bathroomcount, images_url, landlordname, path, postcode, rentpcm, processed, toolkitid, sourcename)VALUES ("+str(id)+",'"+availableFrom+"', "+str(bathroomcount)+", '"+imagefileURLTablet+"', '"+Landlordname+"', '"+path+"', '"+str(postCode)+"',"+str(rentpcm)+"," + str(processed)+",'"+toolkidID+"','"+sourceName+"')"                               
                                ##print(insert)
                                #cur.execute(insert) 
                                

    conn.commit()
    cur.close()
    conn.close()
    f.close()

def Main():
    startCrawler()

Main()



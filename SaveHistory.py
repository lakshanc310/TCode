import requests
import json
import psycopg2
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
cur = conn.cursor(cursor_factory=RealDictCursor)

def startCrawler():

    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM cities limit 10;') #CHANGE
    Cities = cur.fetchall()

    cur.execute('SELECT * FROM proxies;')#CHANGE
    ProxyList = cur.fetchall()
    proxyMap={}

    update_uhresults = "update propertydetails set availabilityflag ='NA'"
    #update_uhresults = "update_uhresults set availabilityflag ='NA'"
    
    cur.execute(update_uhresults)

    for i in range(0,len(ProxyList)):
        proxyMap[i]='http://'+ ProxyList[i]["connect_address"]+':'+ProxyList[i]["connect_port"]

    for City in Cities:
            cityName = (City['extension'])#CHANGE
            print(cityName)
            try:
                response = requests.get('https://www.unihomes.co.uk/student-accommodation/'+cityName+'?page=1&reload=true', headers=headers,proxies=proxyMap, timeout=TIMEOUT_IN_SECONDS)
            except (ProxyError, ReadTimeout, ConnectTimeout) as error:
                    print('Unable to connect to the proxy: ', error)
            else:
                f = open("history.txt", "w")
                f.write(str(response.content.decode()))
                f = open('history.txt')
                data = json.load(f)
      
                for i in data['properties']:
                    id = i['id']
                    rooms = int(i['roomsAvailableCount'])
                    rentpcm = (round(float(i['price']),2) *rooms*52)/12 
                    #CHANGE
                    selectString = "select rentpcm  from propertydetails where id ="+str(id)+ " limit 1"
                    cur.execute(selectString)
                    rentPCM_old = cur.fetchone()
                    if(float(rentpcm) != rentPCM_old["rentpcm"]):
                        #select record and check if price is changed and insert into history table 
                        if(float(rentpcm) > rentPCM_old["rentpcm"]):#CHANGE
                            #CHANGE
                            update_uhresults = "update propertydetails set availabilityflag ='A' where id = '"+str(id)+"'"
                            insertString_History = "INSERT INTO public.updatehistory(propertyid, newprice, lastupdateddate, status, removed)VALUES ('"+str(id)+"', '"+str(rentpcm)+"', NOW()::date ,'increaed',0);"
                        else:
                            #CHANGE
                            insertString_History = "INSERT INTO public.updatehistory(propertyid, newprice, lastupdateddate, status, removed)VALUES ('"+str(id)+"', '"+str(rentpcm)+"', NOW()::date ,'reduced',0);"
                            update_uhresults = "update propertydetails set availabilityflag ='A' where id = '"+str(id)+"'"
                        
                        cur.execute(insertString_History)
                    else:
                        update_uhresults = "update propertydetails set availabilityflag ='A' where id = '"+str(id)+"'"
                    cur.execute(update_uhresults)    

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
                            print('Unable to connect to the proxy: ', error)
                        else:
                            f = open("history.txt", "w")
                            f.write(str(response.content.decode()))
                            f = open('history.txt')
                            data = json.load(f)
                            
                            for i in data['properties']:
                                id = i['id']                           
                                rooms = int(i['roomsAvailableCount'])
                                #rent per week x rooms x 52 weeks / 12 months
                                rentpcm = (round(float(i['price']),2) *rooms*52)/12 
                                #CHANGE
                                selectString = "select rentpcm  from propertydetails where id ="+str(id)+ " limit 1"
                                cur.execute(selectString)
                                rentPCM_old = cur.fetchone()
                                if(float(rentpcm) != rentPCM_old["rentpcm"]):
                        #select record and check if price is changed and insert into history table 
                                    if(float(rentpcm) > rentPCM_old["rentpcm"]):#CHANGE
                                    #CHANGE
                                        update_uhresults = "update propertydetails set availabilityflag ='A' where id = '"+str(id)+"'"
                                        insertString_History = "INSERT INTO public.updatehistory(propertyid, newprice, lastupdateddate, status, removed)VALUES ('"+str(id)+"', '"+str(rentpcm)+"', NOW()::date ,'increaed',0);"
                                    else:
                                    #CHANGE
                                        insertString_History = "INSERT INTO public.updatehistory(propertyid, newprice, lastupdateddate, status, removed)VALUES ('"+str(id)+"', '"+str(rentpcm)+"', NOW()::date ,'reduced',0);"
                                        update_uhresults = "update propertydetails set availabilityflag ='A' where id = '"+str(id)+"'"
                                
                                    cur.execute(insertString_History)
                                else:
                                    update_uhresults = "update propertydetails set availabilityflag ='A' where id = '"+str(id)+"'"
                                cur.execute(update_uhresults)  



    f.close()

def Main():
    startCrawler()
    CheckForMissingProp()
    conn.commit()
    cur.close()
    conn.close()

def CheckForMissingProp():
     #Flag what is missing when updating history table
     selectString = "select id from public.propertydetails where availabilityFlag = 'NA'" #CHANGE
     cur.execute(selectString)
     propertyIDList = cur.fetchall()
     for row in propertyIDList:
        insertString_History = "INSERT INTO public.updatehistory(propertyid, newprice, lastupdateddate, status, removed)VALUES ('"+str(row["id"])+"', '0', NOW()::date ,'let',1);"
        cur.execute(insertString_History)


Main()

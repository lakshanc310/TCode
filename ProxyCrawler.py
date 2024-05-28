import requests
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from requests.exceptions import ProxyError, ReadTimeout, ConnectTimeout
import string
from datetime import date

#CHANGE
conn = psycopg2.connect(database = "UniHomes", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "admin",
                        port = 5432)

TIMEOUT_IN_SECONDS = 10
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
quotes = ["'", '"']

def dateChanger(dateInStr):

    if(dateInStr[3] == " "):
        dd = dateInStr[0:1]
        mm = dateInStr[3:-5]
        yyyy = dateInStr[-4:]
        
    else:
        dd = dateInStr[0:2]
        mm = dateInStr[5:-5]
        yyyy = dateInStr[-4:]
    if(mm.lower().strip() == "january"):
        mm='01'
    elif(mm.lower().strip() == "february"):
         mm='02'
    elif(mm.lower().strip() == "march"):
         mm='03'
    elif(mm.lower().strip() == "april"): 
         mm='04'
    elif(mm.lower().strip() == "may"):
         mm='05'
    elif(mm.lower().strip() == "june"):
         mm='06'
    elif(mm.lower().strip() == "july"):
         mm='07'
    elif(mm.lower().strip() == "august"):
         mm='08'
    elif(mm.lower().strip() == "september"):
         mm='09'
    elif(mm.lower().strip() == "october"):
         mm='10'
    elif(mm.lower().strip() == "november"):
         mm='11'
    else:
        mm='12'
    return (dd+"/"+mm+"/"+yyyy)

def startCrawler():

    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM cities limit 10;') #CHANGE
    Cities = cur.fetchall()

    cur.execute('SELECT * FROM proxies;')#CHANGE
    ProxyList = cur.fetchall()
    proxyMap={}

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
                f = open("jsonfilewrite.txt", "w")
     
                if response.status_code == 200:                  
                    f.write(str(response.content.decode()))
                    f = open('jsonfilewrite.txt')
                    data = json.load(f)
                    for i in data['properties']:
                        availableFrom = i['availableFrom'] 
                        if(availableFrom.lower() != "available immediately"):
                             availableFrom = dateChanger(availableFrom[15:])
                        else:
                            today = date.today()
                            availableFrom = today.strftime("%d/%m/%Y")
                            
                        bathroomcount = i['bathroomCount']              
                        imagefileURLTablet =  i['images'][0]['src']['original']['url']
                        #if company name is not available use fname and lname
                        if(i['landlord']['company'] != ""):
                            Landlordname = i['landlord']['company']
                        else:
                            Landlordname = i['landlord']['first_name'] + i['landlord']['last_name']
                        temp = ""
                        for character in Landlordname:
                            if character not in quotes:
                                temp += character
                        Landlordname = temp
                        id = i['id']
                        path = i['path']
                        postCode = i['postcode']                    
                        rooms = int(i['roomsAvailableCount'])
                        rentpcm = (round(float(i['price']),2) *rooms*52)/12 
                        processed = "0"
                        removed = "0"
                        toolkidID = 0
                        sourceName = "UniHomes"
                        #CHANGE
                        #insertString = "INSERT INTO public.propertydetails(id, availablefrom, bathroomcount, images_url, landlordname, path, postcode, rentpcm, processed, toolkitid, sourcename)VALUES ("+str(id)+",'"+str(availableFrom)+"', "+str(bathroomcount)+", '"+imagefileURLTablet+"', '"+Landlordname+"', '"+path+"', '"+str(postCode)+"',"+str(rentpcm)+"," + str(processed)+",'"+toolkidID+"','"+sourceName+"')"
                        insertString = "INSERT INTO public.uhresults(availablefrom, bathrooms, images, landlord, unihomesid, id, url, postcode, rentpcm, removed, processed, toolkitid, source)VALUES ('"+availableFrom+"', "+str(bathroomcount)+", '"+imagefileURLTablet+"', '"+Landlordname+"',"+str(id)+", "+str(id)+",'"+path+"', '"+str(postCode)+"',"+str(rentpcm)+","+str(removed)+"," + str(processed)+",'"+str(toolkidID)+"','"+sourceName+"')"
                        #print(insertString)
                        cur.execute(insertString)
                        
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
                                    availableFrom = i['availableFrom'] 
                                    if(availableFrom.lower() != "available immediately"):
                                        availableFrom = dateChanger(availableFrom[15:])
                                    else:
                                        today = date.today()
                                        availableFrom = today.strftime("%d/%m/%Y")
                                    bathroomcount = i['bathroomCount']
                                    imagefileURLTablet =  i['images'][0]['fileURLTablet'] 
                                    if(i['landlord']['company'] != ""):
                                        Landlordname = i['landlord']['company']
                                    else:
                                        Landlordname = i['landlord']['first_name'] + i['landlord']['last_name']
                                    temp = ""
                                    for character in Landlordname:
                                        if character not in quotes:
                                            temp += character
                                    Landlordname = temp
                                    path = i['path']
                                    postCode = i['postcode']
                                    rooms = int(i['roomsAvailableCount'])
                                    print('price - >',i['price'])
                                    rentpcm = (round(float(i['price']),2) *rooms*52)/12 
                                    print('price - >',i['price'])
                                    processed = 0
                                    toolkidID = 0
                                    sourceName = "Uni Homes"
                                    #CHANGE
                                    #insert = "INSERT INTO public.propertydetails(id, availablefrom, bathroomcount, images_url, landlordname, path, postcode, rentpcm, processed, toolkitid, sourcename)VALUES ("+str(id)+",'"+availableFrom+"', "+str(bathroomcount)+", '"+imagefileURLTablet+"', '"+Landlordname+"', '"+path+"', '"+str(postCode)+"',"+str(rentpcm)+"," + str(processed)+",'"+toolkidID+"','"+sourceName+"')"                                                                                                                                                                                                                #availablefrom, bathrooms, images, landlord, unihomesid, id, url, postcode, rentpcm, removed, processed, toolkitid, source                                                  
                                    insert = "INSERT INTO public.uhresults(availablefrom, bathrooms, images, landlord, unihomesid, id, url, postcode, rentpcm, removed, processed, toolkitid, source)VALUES ('"+availableFrom+"', "+str(bathroomcount)+", '"+imagefileURLTablet+"', '"+Landlordname+"',"+str(id)+", "+str(id)+",'"+path+"', '"+str(postCode)+"',"+str(rentpcm)+","+str(removed)+"," + str(processed)+",'"+str(toolkidID)+"','"+sourceName+"')"
                                    cur.execute(insert) 
                                    

    conn.commit()
    cur.close()
    conn.close()
    f.close()

def Main():
    startCrawler()

Main()



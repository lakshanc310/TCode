import requests
import csv
from requests.exceptions import ProxyError, ReadTimeout, ConnectTimeout
TIMEOUT_IN_SECONDS = 10
PROXY = 'http://190.233.17.137:999'
CSV_FILE = 'proxies.csv'
with open(CSV_FILE) as open_file:
    reader = csv.reader(open_file)
    for csv_row in reader:
        scheme_proxy_map = {
            'https': csv_row[0],
        }
        
        # Access the website via proxy
        try:
            response = requests.get(
            'https://ip.oxylabs.io/location',
              proxies=scheme_proxy_map,
              timeout=TIMEOUT_IN_SECONDS)
        except (ProxyError, ReadTimeout, ConnectTimeout) as error:
            pass
        else:
            print("Hello")
            print(response.text)
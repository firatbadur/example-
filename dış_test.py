from bs4 import BeautifulSoup
import ssl
import json
import requests
import urllib3
ranges = []

username = 'admin'
password = '1234'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = 'https://burdursais.onlinecevre.com.tr/v1/site/1/channelrange'
r = requests.get(url, auth=(username, password),verify = False)

page = r.content

ssl._create_default_https_context = ssl._create_unverified_context
soup = BeautifulSoup(page, 'html.parser')
person_dict = json.loads(str(soup))
deger = person_dict['channels_range']
new = deger['channels']


i = 0
while (i < len(new)):
    res_1 = new[i]['id']
    res_2 = new[i]['name']
    res_3 = new[i]['min_range']
    res_4 = new[i]['max_range']
    res_5 = new[i]['signal_min']
    res_6 = new[i]['signal_max']
    res_7 = new[i]['factor']
    res_8 = new[i]['channel_row']

    all = (res_1, res_2, res_3, res_4, res_5 ,res_6 ,res_7 ,res_8)
    global ranges
    ranges.append(all)
    i += 1

print(ranges)
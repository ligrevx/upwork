#!/usr/local/bin/python3

import json, os, pandas, re, requests
from lxml import html

proxy = {'https': os.getenv('httpproxy')}
headers = {"Host": "www.webmd.com", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0", "Accept": "application/json, text/plain, */*", "Origin": "https://doctor.webmd.com", "Referer": "https://doctor.webmd.com/"}

persons = []

def search(params):   
   req = requests.get("https://www.webmd.com/search/2/api/lhd_v_search", params=params, headers=headers, proxies=proxy)
   dat = json.loads(req.text)
   for man in dat['data']['response']:
      assn = [json.loads(i) for i in man['location_nimvs'] if i]
      addr = assn[0]
      phone = addr['LocationPhone']
      address = '%s, %s, %s, %s, %s' % (addr['PracticeName'], addr['address'], addr['city'], addr['state'], addr['zipcode'])
      person = {'Physician Name': man['fullname'], 'Specialty': man['specialty_consumername_mvs'][0], 'Phone': phone, 'Address': address, 'LocationId': addr['LocationId'], "LocationEntityId": addr["LocationEntityId"]}      
      persons.append(person)      
      with open('datadump.txt', 'a') as p:
         p.write("%s,\n" % person)
         print('writing: %s' % person)

   
for start in range(0, 36, 10):
   params = {"sortby": "bestmatch", "distance": 161, "newpatient": "", "minrating":0, "start": start, "q": "Physical Medicine and Rehabilitation", "pt": "39.1836,-96.5716", "specialtyid":29309, "insuranceid": ""}
   search(params)

# search range(0, 75, 10): params = {"sortby": "bestmatch", "distance": 40, "newpatient": "", "minrating":0, "start": start, "q": "Neurologist", "pt": "30.6739,-88.089", "specialtyid": 29282, "insuranceid": ""}
# search range(0, 67, 10): params = {"sortby": "bestmatch", "distance": 161, "newpatient": "", "minrating":0, "start": start, "q": "Physical Medicine & Rehabilitation", "pt": "30.6739,-88.089", "specialtyid":29309, "insuranceid": ""}

pandas.read_json(json.dumps(persons)).to_excel("datadump_physical_medicine_and_rehabilitation_mahattan.xlsx", index=False)

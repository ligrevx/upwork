#!/usr/local/bin/python3

import json, os, pandas, re, requests
from lxml import html

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"

persons = []

def search(page):
   req = requests.post("http://www.osbar.org/members/membersearch.asp?bar=&first=&last=&scity=Eugene&pastnames=&cp=%d" % page, headers={'user-agent': ua})
   htm = html.fromstring(req.text)
   for bid in htm.xpath('//table[@id="tblResults"]//tr/td[1]/text()'):
      nom = htm.xpath('//table[@id="tblResults"]//tr[contains(., "%s")]/td[2]/text()' % bid)
      person(bid, nom)

def person(bid, nom):
   req = requests.get("http://www.osbar.org/members/membersearch_display.asp?b=%s" % bid, headers={'user-agent': ua})
   htm = html.fromstring(req.text)
   stat = htm.xpath('//tr/td[@id="mstatus"]/text()')
   status = ''.join(stat).lower()

   if 'active member' in status:       
      com = htm.xpath('//tr[contains(.,"Company")]/td[2]/text()')
      adr = htm.xpath('//tr[contains(.,"Address")]/td[2]/text()')
      eml = htm.xpath('//tr/td[@id="memail"]/a/text()')
      fon = htm.xpath('//tr/td[@id="mphone"]/text()')

      last, first = ''.join(nom).split(',')
      fn = re.sub('\w{2,3}\.\s', '', first.strip())
      ln = last.strip()

      dat = {'firstname': fn, 'lastname': ln, 'company': ''.join(com), 'address': ', '.join(adr).replace("\u00a0", " "), 'email': ''.join(eml), 'phone': ''.join(fon)}

      if not dat['company']:
         dat['company'] = 'N/A'
      if not dat['address']:
         dat['address'] = 'N/A'
      if not dat['phone']:
         dat['phone'] = 'N/A'

      if dat['email']:       
         persons.append(dat)
         print('saving: %s' % dat)
         dat['bid'] = bid
         with open('datadump.txt', 'a') as p:
            p.write("%s,\n" % dat)


for i in range(1,62):
   search(i)

pandas.read_json(json.dumps(persons)).to_excel("datadump.xlsx", index=False)

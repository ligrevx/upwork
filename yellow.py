#!/usr/bin/env python3

import json, os, pandas, re, requests, time
from lxml import html

ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
yp = "https://www.yellowpages.com.au/search/listings?clue=Gift+Shop&locationClue=All+States&pageNumber={}"
of = "yellow_{}.xlsx".format(int(time.time()))

items = []

def aa(url):
  req = requests.get(url, headers={'user-agent': ua})
  dat = html.fromstring(req.text)
  num = 0

  print('scanning {}'.format(url))

  for each in dat.xpath("//div[contains(@class,'MuiCard-root')]"):
    name = each.xpath(".//h3[contains(@class,'MuiTypography-h3')]//text()")
    addr = each.xpath(".//p[contains(@class,'MuiTypography-body2')]//text()")
    tele = each.xpath(".//a[contains(@class,'ButtonPhone')]/@href")
    kwrd = each.xpath(".//p[contains(@class,'MuiTypography-subtitle2')]//text()")

    if type(name) == list:
      name = ''.join(name)

    if type(addr) == list:
      addr = ''.join(addr)

    if type(tele) == list:
      tele = ''.join(tele)

    if type(kwrd) == list:
      kwrd = ''.join(kwrd)

    if len(name) == 0:
      break

    item = { "Name": name, "Address": addr, "Contact": tele, "Keyword": kwrd }

    items.append(item)

    num = num + 1

  print("### total items from this page : {}".format(num))

def ss():

  print('Saving as {}'.format(of))

  pandas.read_json(json.dumps(items)).to_excel(of, index=False)


def st():
  for p in range(1,71):
    aa(yp.format(p))

  ss()

st()

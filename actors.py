#!/usr/local/bin/python3

import json, os, re, requests
from lxml import html

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"

persons = []

def index():
   req = requests.post("https://en.wikipedia.org/wiki/List_of_Filipino_actors", headers={'user-agent': ua})
   dat = html.fromstring(req.text)
   for each in dat.xpath('//div[contains(@class,"columns")]/ul/li/a'):
      person(each.text, each.get('href'))

   with open("actors.json", "w") as people:
      json.dump(persons, people)
      
def person(name, wiki):
   persons.append({"name": name, "wiki": wiki})

def read()
   with open("actors.json") as actors:
      people = json.loads(actors.read())
      for person in people:
         print(person['name'], person['wiki'])

if __name__ == "__main__":
   index()

#!/usr/bin/env python
# encoding: utf-8
"""
gscholar.py

Created by Andrew Ning on November 16, 2013
"""


import requests
import alfred
from bs4 import BeautifulSoup  # , SoupStrainer
import hashlib
import random
import sys

from common import waitForPeriodInQuery


# get query from user (won't parse until ends with ".")
title='Google Scholar Search'
icon = 'gscholar.png'
query = waitForPeriodInQuery(title, icon)


params = {'q': query}

# set headers (thank you: http://blog.venthur.de/index.php/2010/01/query-google-scholar-using-python/)
google_id = hashlib.md5(str(random.random())).hexdigest()[:16]
headers = {'User-Agent': 'Mozilla/5.0',
           'Cookie': 'GSP=ID=%s:CF=4' % google_id}


# search on google cscholar
proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"}
r = requests.get('http://scholar.google.com/scholar', params=params, headers=headers, proxies=proxies)
# r.encoding = 'utf-8'

# parse data
# only_articles = SoupStrainer('div', {'class': 'gs_r'})
# articles = BeautifulSoup(r.text, 'html.parser', parse_only=only_articles)
soup = BeautifulSoup(r.text, 'html5lib')

# get all articles
articles = soup.find_all('div', {'class': 'gs_r'})

results = []
for art in articles:

    data = art.find('div', {'class': 'gs_ri'})

    if data is None:
        continue  # skip this one

    # get title
    # title = art.find('h3', {'class': 'gs_rt'}).a.contents[0]
    title = data.find('h3', {'class': 'gs_rt'})
    title = ''.join(title.findAll(text=True))
    if title[0] == '[':
        entries = title.split(']')
        title = entries[0] + ']' + entries[2]

    # author data
    author_fields = data.find('div', {'class': 'gs_a'})
    author_data = ''.join(author_fields.findAll(text=True))  # .encode('utf-8')

    # bibtex link
    links = data.find('div', {'class': 'gs_fl'})
    bibtex_link = links.find('a', href=True, text='Import into BibTeX')['href']

    # a unique id
    some_id = bibtex_link.split(':')[2]
    arg = bibtex_link

    results.append(alfred.Item(title=title,
                               subtitle=author_data,
                               attributes={'uid': some_id, 'arg': arg},
                               icon='gscholar.png'))

alfred.write(alfred.xml(results))

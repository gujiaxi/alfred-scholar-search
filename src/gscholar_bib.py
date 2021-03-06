#!/usr/bin/env python
# encoding: utf-8
"""
bib_gscholar.py

Created by Andrew Ning on November 16, 2013
"""

import sys
import requests
import hashlib
import random


# get the links
bibtex_link = sys.argv[1]

# set headers (thank you: http://blog.venthur.de/index.php/2010/01/query-google-scholar-using-python/)
google_id = hashlib.md5(str(random.random())).hexdigest()[:16]
headers = {'User-Agent': 'Mozilla/5.0',
           'Cookie': 'GSP=ID=%s:CF=4' % google_id}

# grab bibtex
r = requests.get(bibtex_link, headers=headers)
bibtex = r.text

# show bibtex
sys.stdout.write(bibtex)
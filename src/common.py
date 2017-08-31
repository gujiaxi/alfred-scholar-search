#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by Andrew Ning on 2013-11-17.
"""

import sys
from subprocess import Popen, PIPE
import re
import requests
import os
import time
import alfred



months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def waitForPeriodInQuery(title, icon=None):
    """waits for user to end query with '.' before actually initiating search"""

    # get query from user
    query = sys.argv[1]

    if icon is None:
        icon = 'icon.png'

    if query[-1] != '.':

        results = [alfred.Item(title=title,
                           subtitle="end query with . to execute search",
                           attributes={'uid': 'none'},
                           icon=icon)]

        sys.stdout.write(alfred.xml(results))
        exit()

    return query[:-1]


def runAppleScript(script):
    Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE).communicate(script)

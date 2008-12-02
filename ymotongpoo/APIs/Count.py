# -*- encoding: utf-8 -*-
"""
Count.py



Known issue:
    - getUpdate()
      'uri' elements cannot be get
"""

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2008/12/02 00:48:52$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import random, datetime, time
import base64, sha
import urllib, httplib
from xml.dom import minidom

SITE_URL = 'http://www.benricho.org/kazu/database/kazu_database.cgi'

def searchCounterSuffix(key):
    get_dict = dict( key = key,
                     select = 50)
    params = urllib.urlencode(get_dict)
    f = urllib.urlopen(SITE_URL + '?' + params)
    print f.read()

def main():
    key = urllib.quote_plus(unicode('帽子', 'utf-8').encode('shift_jis'),':;/')
    searchCounterSuffix(key)

if __name__ == '__main__':
    main()

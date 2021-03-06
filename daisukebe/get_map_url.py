# -*- coding: utf-8 -*-
import sys
import re
import urllib
from BeautifulSoup import BeautifulSoup

def get_maps_url(address):
    url_list = ['http://maps.google.co.jp/maps?q=' + a for a in address]

    return url_list

def get_store_name(soup):
    name = []
    for ss in [s for s in soup.findAll("a")]:
        l = len(ss)
        if l == 1:
            name.append(ss.contents[0].__str__())
        elif l == 3:
            name.append(ss.contents[0].__str__() + ss.contents[2].__str__())

    return name

def get_store_address(soup):
    x = [s for s in soup('span')]
    y = x[2:]
    z = [y[n] for n in range(len(y)) if n % 2 == 0]

    address = []
    for a in z:
        address.append(a.contents[0].__str__())

    return address

def main(*argv):
    b = {'key_word': (u'三宮'.encode('shift-jis'))}
    url = 'http://www.sevenbank.co.jp/www-cgi/a012.php?sub_option=&'\
        + urllib.urlencode(b) + '&area_code=&qzip=&sql_flg=1&fst_store_csol=&store_cnt=1&city_code='

    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    
    store = get_store_name(soup)
    address = get_store_address(soup)

    url_list = get_maps_url(address)

    for u in url_list:
        print u

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

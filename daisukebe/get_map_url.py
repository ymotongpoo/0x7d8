# -*- coding: utf-8 -*-
import sys
import re
import urllib
from BeautifulSoup import BeautifulSoup

def get_maps_url(address):
    url_list = ['http://maps.google.co.jp/maps?q=' + a + \
                    '&um=1&ie=UTF-8&hq=&hnear=' + a +\
                    '&gl=jp&ei=mcf-SoSJJY-pkAXv-OXuCw&sa=\
X&oi=geocode_result&ct=title&resnum=1&ved=0CAgQ8gEwAA'
                for a in address]

    return url_list

"""
def get_store_name_(soup):
    name = []
    for ss in [s for s in soup.findAll("a")]:
        store_ = re.sub('<a\shref=\"z001\.php\?cmpny_cd=[0-9]\
{4}&amp\;store_cd=[0-9]{6}&amp;rmode=[0-9]\
&amp;pg=[a-z][0-9]{4}\"\starget=\"_top\">',
                        '',
                        ss.__str__())
        store__ = re.sub('<br\s/>', '', store_)
        name.append(re.sub('</a>', '', store__))
    
    return name
"""
def get_store_name(soup):
    name = []
    for ss in [s for s in soup.findAll("a")]:
        l = len(ss)
        if l == 1:
            name.append(ss.contents[0].__str__())
        elif l == 3:
            name.append(ss.contents[0].__str__() + ss.contents[1].__str__())


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
    b = {'key_word': (u'渋谷'.encode('shift-jis'))}
    url = 'http://www.sevenbank.co.jp/www-cgi/a012.php?sub_option=&'\
        + urllib.urlencode(b) + '&area_code=&qzip=&sql_flg=1&\
fst_store_csol=&store_cnt=1&city_code='

    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    
    store = get_store_name(soup)
    address = get_store_address(soup)

    url_list = get_maps_url(address)

    for u in url_list:
        print u

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

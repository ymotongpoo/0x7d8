#
# -*- coding: utf8 -*-;
#
# Twitter XML Logger in Python
#
# Yoshifumi YAMAGUCHI @ymotongpoo
#

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2010/09/20 22:43:10$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

from time import sleep
import os
import urllib
import re
from StringIO import StringIO
from lxml import etree

xml_header = '<?xml version="1.0" encoding="UTF-8"?>'

twitter_api = 'http://api.twitter.com/1/statuses/user_timeline.xml?'

default_options = {'screen_name':'ymotongpoo',
                   'trim_user':'false',
                   'include_rts':'true',
                   'include_entities':'true',
                   'max_id':'9'*1,
                   'since_id':'0'
                   'count':'200'
                   }

interval = 25 # interval sec. for each HTTP request

def update_option(**options):
    """
    update GET options for Twitter API
    @param options dictionary of options
    """
    api_options = default_options

    for k,v in option.iteritems():
        if k in default_options:
            api_options[k] = v

    return api_options


def retreive_xml(**options):
    """
    retreive timeline in xml format via twitter api
    @param options dictionary of options
    """
    get_query = []
    for k, v in options.iteritems():
        get_query.append(k + '=' + v)

    url = twitter_api + '&'.join(get_query)
    p = urllib.urlopen(url)
    content = p.read()
    return content


def minimum_id(tweets):
    """
    find minimum id from xml
    @param tweets retreived xml
    """
    try:
        tree = etree.parse(StringIO(tweets), etree.XMLParser())
        statuses = tree.xpath('//statuses')
        id_str = statuses[0].xpath('./status/id/text()')
        ids = []
        for id in id_str:
            ids.append(int(id))
        return str(min(ids))

    except IndexError, e:
        raise e
    except ValueError, e:
        raise e


def delete_first_line(string):
    """
    delete head line from assigned lines
    @param lines string
    """
    lines = string.split('\n')
    return '\n'.join(lines[1:])


def past_retreiver(max_id):
    options = default_options
    del options['since_id']
    options['max_id'] = str(max_id)
    return retreive_xml(**options)


def future_retreiver(since_id):
    options = default_options
    del options['max_id']
    options['since_id'] = str(since_id)
    return retreive_xml(**options)


def runner(id = -1, filename = 'twitter.log', direction = 'past'):
    """
    runner retreives all tweets 
    """
    if os.path.isfile(filename):
        fp = open(filename, 'a+')
    else:
        fp = open(filename, 'wa+')
        fp.write(xml_header)
    try:
        if id==-1:
            print '...done'
            return
        else:
            if direction == 'past':
                xml = past_retreiver(id)
            elif direction == 'future':
                xml = future_retreiver(id)
            else:
                return
            xml = delete_first_line(xml)
            fp.write(xml)
            fp.close()

            min_id = minimum_id(xml)
            print min_id
            
            sleep(interval)
            runner(int(min_id)-1)

    except IndexError, e:
    except ValueError, e:
    except Exception, e: # for "Twitter is over capacity"
        print xml
        fp.close()
        sleep(interval)
        runner(id=id)


if __name__ == '__main__':
    runner(id = 99999999999)

# -*- coding: utf-8 -*-;
#
# log2blgr.py  ---  post twitter log to Blogger
#
# external packages
#   - gdata-python-client
#
# API reference
# 1. Google Data API Python Client Library
#   http://code.google.com/p/gdata-python-client/
#
# ToDo
#   1. create in-reply-to link -- version 1.0
#   2. retrieve original urls from shorten ones -- version 1.1
#   3. get conversations -- version 2.0
#

__author__  = 'ymotongpoo <ymotongpoo AT gmail DOT com>'
__version__ = '0.9'
__date__    = '2009/11/19 (Thu)'

from gdata import service, client
from gdata.blogger import client
import gdata
import atom

from datetime import datetime, timedelta
import re
import sys
import getopt
from os import path

TITLE = '[Twitter] %s'
LOG_TIME_FMT = '%Y-%m-%dT%H:%M:%S'
TIME_FMT = '%H:%M:%S'
TWITER_ID = 'ymotongpoo'
STATUS_URL = 'http://twitter.com/%s/statuses/%s'

DECODING = 'utf-8'
ENCODING = 'utf-8'

class BloggerOperator:
    def __init__(self, email=None, password=None):
        self.blogger_service = None
        self.email = email
        self.password = password

    def ClientLogin(self, email=None, password=None):
        if not email:
            email = self.email
        if not password:
            password = self.password
        self.blogger_service = service.GDataService(email, password)
        self.blogger_service.source = 'LOG2BLGR'
        self.blogger_service.service = 'blogger'
        self.blogger_service.accout_type = 'GOOGLE'
        self.blogger_service.server = 'www.blogger.com'
        self.blogger_service.ProgrammaticLogin()

    def CreatePublicPost(self, title, content):
        query = service.Query()
        query.feed = '/feeds/default/blogs'
        feed = self.blogger_service.Get(query.ToUri())
        blog_id = feed.entry[0].GetSelfLink().href.split('/')[-1]

        entry = gdata.GDataEntry()
        entry.title = atom.Title('xhtml', title)
        entry.content = atom.Content(content_type='html', text=content)
        return self.blogger_service.Post(entry, '/feeds/%s/posts/default' % blog_id)


def log2content(filename, log_path='.'):
    def format_time(timestr, id):
        time = datetime.strptime(timestr, LOG_TIME_FMT)
        status_url = STATUS_URL % (TWITER_ID, id)
        time_str = '<a href="%s">%s</a>' % (status_url, time.strftime(TIME_FMT))
        return time_str

    def format_link(text):
        urls = re.findall(r"s?https?://[-_.!~*'()a-zA-Z0-9;/?:@&=+$,%#]+", text)
        fixed = text
        for u in urls:
            link = u'<a href="%s">%s</a>' % (u, u)
            fixed = fixed.replace(u, link)
        return fixed

    def format_reply(text, in_reply_to_id, in_reply_to_user):
        replies = re.findall(r"@[_a-zA-Z0-9]]+", text)
        fixed = text
        for r in replies:
            user = r.spilt('@').pop()
            link = u'<a href="http://twitter.com/%s">%s</a>' % (user, r)
            fixed = fixed.replace(r, link)

        if in_reply_to_id:
            url = STATUS_URL % (in_reply_to_user, in_reply_to_id)
            fixed += u' (in reply to <a href="%s">%s</a>)' % (url, in_reply_to_user)
        return fixed
    
    log = path.join(log_path, filename)
    f = open(log, 'r')
    tweets = u''
    for l in f.readlines():
        l = l.decode(DECODING)
        item = u''

        content = l.split('\t')
        id = content[0]
        tweet = format_link(content[1])
        #tweet = format_reply(tweet, content[3])
        time_str = format_time(content[2], id)
        item = '<li>%s : %s</li>' % (time_str, tweet)
        tweets += item
    
    content = u'<ul>%s</ul>' % tweets
    content += '\nLOG2BLGR ver.' + __version__
    return content


def process(email, password, title, content):
    blgr = BloggerOperator(email, password)
    blgr.ClientLogin()
    blgr.CreatePublicPost(title, content)


def usage():
    print 'usage : python log2blgr.py -e <email address> -p <password> -l <log dir path>\n'
    print 'log file name is thought to be "YYYYMMDD.log", which date is yesterday.'

if __name__=='__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    else:
        try:
            try:
                opts, opt_args = getopt.getopt(sys.argv[1:], 'e:p:l:')
            except getopt.GetoptError:
                print 'usage error'
                usage()
                sys.exit(2)
                
            for o, v in opts:
                if o == '-e':
                    email = v
                elif o == '-p':
                    password = v
                elif o == '-l':
                    log_path = v
        
            yesterday = datetime.today() - timedelta(days=1)
            title_date = yesterday.strftime('%Y-%m-%d (%a)')
            log_name = yesterday.strftime('%Y%m%d') + '.log'

            title = TITLE % title_date
            content = log2content(log_name, log_path)
        
            process(email, password, title, content)
        except Exception, e:
            print e
            sys.exit(2)


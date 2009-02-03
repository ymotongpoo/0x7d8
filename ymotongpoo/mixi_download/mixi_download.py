#-*- encoding: utf-8 -*-;
__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2009/02/02 22:43:10$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import urllib
import re
from HTMLParser import HTMLParser, HTMLParseError

MONTH = {'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'}

YEAR = range(2005, 2010)

class MixiOpener(urllib.FancyURLopener):
    def login(self, email, password):
        LOGIN_URL = 'http://mixi.jp/login.pl'
        params = urllib.urlencode({
            'email': email,
            'password': password,
            'next_url': 'home.pl'})

        r = self.open(LOGIN_URL, params)
        cookie = []
        for c in r.headers.getheaders('Set-Cookie'):
            m = re.match('(.+=.+);.*', c)
            if m:
                cookie.append(m.groups()[0])

        self.addheader('Cookie', ';'.join(cookie))
        r = self.open('http://mixi.jp/check.pl?n=home.pl')
        return r.read()


class MixiExtractor():
    class ExtractEntryUrl(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.codec = 'euc-jp'
            self.view_url_r = re.compile('^view_diary.pl\?id=[0-9]+&owner_id=[0-9]+$')

            self.urls = []

            self.in_diary_title = False

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if 'div' == tag and 'class' in attrs:
                if 'listDiaryTitle' == attrs['class']:
                    self.in_diary_title = True

            if 'a' == tag and 'href' in attrs and self.in_diary_title:
                if self.view_url_r.match(attrs['href']) != None:
                    self.urls.append(attrs['href'])

        def handle_endtag(self, tag):
            if 'div' == tag and self.in_diary_title:
                self.in_diary_title = False

        def handle_data(self, data):
            pass


    class ExtractEntryBody(HTMLParser):
        def __init__(self, comment=False):
            HTMLParser.__init__(self)
            self.codec = 'euc-jp'
            self.comment = comment

            self.entry = {}

            self.in_title = False
            self.in_title_dt = False
            self.in_title_dd = False
            self.in_diary_body = False

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if 'div' == tag and 'class' in attrs:
                if 'listDiaryTitle' == attrs['class']:
                    self.in_title = True

            if 'dt' == tag and self.in_title:
                self.in_title_dt = True

            if 'dd' == tag and self.in_title:
                self.in_title_dd = True

            if 'div' == tag and 'id' in attrs:
                if 'diary_body' == attrs['id']:
                    self.in_diary_body = True

        def handle_endtag(self, tag):
            if 'div' == tag and self.in_title:
                self.in_title = False
                self.entries.append(entry)
                self.entry = {}

            if 'dt' == tag and self.in_title_dt:
                self.in_title_dt = False

            if 'dd' == tag and self.in_title_dd:
                self.in_title_dd = False

        def handle_data(self, data):
            if self.in_title_dt:
                self.entry['title'] = data.decode(self.codec)

            if self.in_title_dd:
                self.entry['date'] = data.decode(self.codec)

            if self.in_diary_body:
                self.entry['body'] += data.decode(self.codec)

    def __init__(self, username, password):
        mo = MixiOpener()
        mo.login(username, password)

    def __extractContents(self, htmlbody, parser):
        try:
            parser = parser
            parser.feed(htmlbody)
            parser.close()
            return parser
        except HTMLParseError, msg:
            print 'Error Message: %s' % msg

    def getMonthEntryUrls(self, year, month):
        # magic number
        offset = 310
        limit = 895
        MONTH_PAGE_URL = u'http://mixi.jp/list_diary.pl'

        urls = []
        i = 1
        while 1:
            params = urllib.urlencode({
                'year': year,
                'month': month,
                'page': i})
            print params
            r = self.open(MONTH_PAGE_URL, params)

            lines = r.readlines()[offset:limit]
            data = '\n'.join(lines)

            page_urls = self.__extractContents(data, self.ExtractEntryUrl()).urls
            if not len(page_urls):
                break
            else:
                urls += page_urls
                i += 1

        return urls

    def getMonthEntryBody(self, entryurls):
        entries = []
        for u in entryurls:
            r = self.open(u)
            lines = r.readlines()[offset:limit]
            data = '\n'.join(lines)
            page_entry = self.__extractContents(data, self.ExtractEntrBody()).entry
            entries.append(page_entry)

        return entries


def downloadMixiEntries(username, password):
    me = MixiExtratcor(username, password)
    for y in YEAR:
        for m, mon in enumerate(MONTH):
            urls = me.getMonthEntryUrls(y, m)
            entries = getMonthEntryBody(urls)

            filename = str(y) + mon + '.txt'
            fp = open(filename)

            for e in entries:
                fp.write(entries.date)
                fp.write(entries.title)
                fp.write(entries.body)

            fp.close()


if __name__ == '__main__':
    downloadMixiEntries('hoge', 'piyo')



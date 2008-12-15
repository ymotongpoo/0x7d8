# -*- coding: utf-8 -*-

import feedparser
import sqlite3
from genshi.template import TemplateLoader
import os
import time

CODING = 'utf-8'
TEMPLATE_DIR = os.path.dirname(__file__)

urllist = [
    u'http://news4vip.livedoor.biz/index.rdf', # 【2ch】ニュー速クオリティ
    u'http://blog.livedoor.jp/dqnplus/index.rdf', # 痛いニュース
    u'http://urasoku.blog106.fc2.com/?xml', # ハムスター速報 ２ろぐ
    u'http://alfalfa.livedoor.biz/index.rdf', # アルファモザイク
    u'http://koerarenaikabe.livedoor.biz/index.rdf', # 超えられない壁
    u'http://kanasoku.blog82.fc2.com/?xml', # カナ速
    u'http://waranote.blog76.fc2.com/?xml', # ワラノート
    u'http://kaisun1192.blog121.fc2.com/?xml', # おはようｗｗｗお前らｗｗｗｗｗｗｗｗ
    u'http://vipvipblogblog.blog119.fc2.com/?xml', # ベア速
    u'http://news4wide.livedoor.biz/index.rdf', # VIPワイドガイド
    u'http://nukohiroba.blog32.fc2.com/?xml', # ヌコニュース
    u'http://aresoku.blog42.fc2.com/?xml' # ちょっとアレなニュース
    ]


def get_feed(rsslist):
    feedlist = []
    for u in rsslist:
        try:
            feedlist.append(feedparser.parse(u))
        except Exception, e:
            sys.exc_info()[0]
            sys.exc_info()[1]
    
    return feedlist


def rss10feed(feed):
    entries = []
    e = {}
    site = dict(title=feed['feed']['title'].encode(CODING),
                url=feed['feed']['link'].encode(CODING))
    
    for e in feed['entries']:
        updated = time.strftime('%H:%M', time.strptime(e['updated'], '%Y-%m-%dT%H:%M:%S+09:00'))
        
        entries.append(dict(title=e['title'].encode(CODING).strip(),
                            summary=e['summary'].encode(CODING),
                            url=e['link'].encode(CODING),
                            updated=updated.encode(CODING),
                            site=site))
    return entries


mapfeedfunc = {
    'livedoor': rss10feed,
    'fc2.com': rss10feed
    }


def main():
    entrylist = []
    for feed in get_feed(urllist):
        feed['feed']['title'].encode(CODING)

        portal = rss10feed
        for k, v in mapfeedfunc.iteritems():
            try:
                feed['feed']['link'].encode(CODING).index(k)
                portal = k
            except:
                continue

        entrylist += mapfeedfunc[portal](feed)
    feed = None

    loader = TemplateLoader([TEMPLATE_DIR])
    tmpl = loader.load(os.path.join(TEMPLATE_DIR, 'template.html'))
    stream = tmpl.generate(entries=entrylist)
    print stream.render('html')

if __name__ == '__main__':
    main()

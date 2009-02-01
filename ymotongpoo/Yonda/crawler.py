#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2008/12/10 00:29:41$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import sqlite3
import os
from HatenaBookmark import HatenaBookmark
from LivedoorClip import LivedoorClip

def main():
    hb = HatenaBookmark()
    lc = LivedoorClip()
    entries = []

    BASE_DIR = os.path.dirname(__file__)
    c = sqlite3.connect(os.path.join(BASE_DIR, 'bookmark.db'))
    cur = c.cursor()

    cur.execute('select * from ttag')
    taglist = cur.fetchall()
    #print taglist

    for idx, tag in taglist:
        print '-'*8, tag
        # hatena bookmark
        print '# hatena bookmark'
        i = 0
        while 1:
            try:
                entries = hb.searchByTag(tag.encode('utf-8'), u'hot', 25*i)
                if len(entries) == 0:
                    break

                for e in entries:
                    t = (e['url'].encode('utf-8'),)
                    cur.execute('select * from tbookmark where url = ?', t)
                
                    if len(cur.fetchall()) > 0:
                        t = (e['user'], e['url'].encode('utf-8'))
                        cur.execute('update tbookmark set user = ? where url = ?', t)
                    else:
                        t = (e['url'].encode('utf-8'), e['title'].encode('utf-8'), e['user'], 0)
                        cur.execute('insert into tbookmark (url, title, user, clip) values (?,?,?,?)', t)
                        c.commit()
                        
            except Exception, e:
                print e
                c.rollback()
                continue

            print 'offset', 25*i
            i += 1

        # livedoor clip
        print '# livedoor clip'
        for i in range(0, 11):
            try:
                entries = lc.searchByTag(tag.encode('utf-8'), u'', i)
                if len(entries) == 0:
                    break

                for e in entries:
                    t = (e['url'].encode('utf-8'),)
                    cur.execute('select * from tbookmark where url = ?', t)

                    if len(cur.fetchall()) > 0:
                        t = (e['user'], e['url'].encode('utf-8'))
                        cur.execute('update tbookmark set clip = ? where url = ?', t)
                    else:
                        t = (e['url'].encode('utf-8'), e['title'].encode('utf-8'), e['user'], 0)
                        cur.execute('insert into tbookmark (url, title, clip, user) values (?,?,?,?)', t)
                        
                        c.commit()

                print 'offset', 20*i
            except Exception, e:
                print e
                c.rollback()
                continue

if __name__ == '__main__':
    main()

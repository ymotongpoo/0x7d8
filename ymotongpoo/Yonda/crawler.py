#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2008/12/10 00:29:41$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import sqlite3
import os
from HatenaBookmark import HatenaBookmark

def main():
    hb = HatenaBookmark()
    entries = []

    BASE_DIR = os.path.dirname(__file__)
    c = sqlite3.connect(os.path.join(BASE_DIR, 'bookmark.db'))
    cur = c.cursor()

    cur.execute('select * from ttag')
    taglist = cur.fetchall()
    print taglist

    for i, tag in taglist:
        i = 0

        print '-'*8, tag
        while 1:
            entries = hb.searchByTag(tag.encode('utf-8'), u'hot', 25*i)
            if len(entries) == 0:
                break

            for e in entries:
                t = (e['url'].encode('utf-8'),)
                cur.execute('select * from tbookmark where url = ?', t)
                
                if len(cur.fetchall()) > 0:
                    t = (e['url'].encode('utf-8'), e['title'].encode('utf-8'), e['user'], e['url'].encode('utf-8'))
                    cur.execute('update tbookmark set url = ?, title = ?, user = ? where url = ?', t)
                else:
                    t = (e['url'].encode('utf-8'), e['title'].encode('utf-8'), e['user'])
                    cur.execute('insert into tbookmark values (?,?,?)', t)

                c.commit()

            print 'offset', 25*i
            i += 1

if __name__ == '__main__':
    main()

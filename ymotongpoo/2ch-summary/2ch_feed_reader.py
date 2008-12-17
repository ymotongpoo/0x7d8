# -*- coding: utf-8 -*-

import sqlite3
from genshi.template import TemplateLoader
from mod_python import apache
import urllib
import time
import os

CODING = 'utf-8'
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_FILE = os.path.join(BASE_DIR, 'template.html')
DATABASE_FILE = os.path.join(BASE_DIR, '2ch-summary.db')

base_query = 'select a.url, a.title, a.summary, a.updated, ' + \
             'b.url as site_url, b.title as site_title ' + \
             'from tentry as a inner join tsite as b ' + \
             'on a.site_id = b.site_id'

def entry(req, sort='updated', offset=0):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    link_index = []
    if sort == 'updated':
        query = base_query + ' order by a.updated desc'
        
        for i in range(1,10):
            getdict = dict(sort=sort,
                           offset=i*10)
            link_index.append(dict(num=i,
                                   link = './entry?' + urllib.urlencode(getdict))
                              )
            
    else:
        query = base_query + ' order by a.updated desc'
        
    query += ' limit 10 offset ' + str(offset)
    cur.execute(query)
    
    entrylist = []
    for row in cur:
        updated = time.strftime('%m/%d %H:%M',time.strptime(row[3], '%Y-%m-%d %H:%M:%S'))
        e = dict(url=row[0],
                 title=row[1],
                 summary=row[2],
                 updated=updated,
                 site_url=row[4],
                 site_title=row[5])
        entrylist.append(e)
        
    loader = TemplateLoader([BASE_DIR])
    tmpl = loader.load(TEMPLATE_FILE)
    stream = tmpl.generate(entries=entrylist, index=link_index)

    req.content_type = 'text/html'
    req.send_http_header()
    req.write(stream.render('html'))

    return apache.OK

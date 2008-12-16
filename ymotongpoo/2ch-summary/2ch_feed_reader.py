# -*- coding: utf-8 -*-

import sqlite3
from genshi.template import TemplateLoader
import os

CODING = 'utf-8'
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_FILE = os.path.join(BASE_DIR, 'template.html')
DATABASE_FILE = os.path.join(BASE_DIR, '2ch-summary.db')

def main():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute('select a.*, b.url as site_url from tentry as a inner join tsite as b '
                'on a.site_id = b.site_id order by a.updated desc')
    entrylist = cur.fetchall()
    
    loader = TemplateLoader([BASE_DIR])
    tmpl = loader.load(TEMPLATE_FILE)
    stream = tmpl.generate(entries=entrylist)
    print stream.render('html')

if __name__ == '__main__':
    main()

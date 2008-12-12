# -*- encoding: utf-8 -*-

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2008/12/10 00:29:41$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"


import sqlite3
from genshi.template import TemplateLoader

conn = sqlite3.connect('bookmark.db')
cur = conn.cursor()

cur.execute('select url, title from tbookmark order by user desc limit 10')
bookmarks = []
for row in cur:
    bookmarks.append(dict(url=row[0], title=row[1]))

loader = TemplateLoader(['./'])
tmpl = loader.load('yonda.tpl')
stream = tmpl.generate(bookmarks=bookmarks)
print stream.render('html')


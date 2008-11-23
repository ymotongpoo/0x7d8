# -*- coding: utf-8; -*-

#
# @author daisukebe
#

import grok
import urllib
import time
import random
from ZODB import FileStorage, DB
from persistent import Persistent
import transaction


class Flickr1(grok.Application, grok.Container):
    pass

class Index(grok.View):
    pass # see app_templates/index.pt

class getPhotos(grok.View):

    word_ = None

    def arc(sef):
        storage = FileStorage.FileStorage('init_photos.fs')
        db = DB(storage)
        connection = db.open()
        root = connection.root()
        
        transaction.begin()
        arc = root['init']
        transaction.commit()
        
        connection.close()
        db.close()
        
        return arc[::-1]
        #return [random.choice(arc) for i in range(len(arc) - 5)]

    def default(self):
        args = {'method' : 'flickr.photos.search',
                'api_key' : '58abc315168ff0008467f003e2d28b04',
                'per_page' : '50',
                'sort' : 'date-posted-desc',
                'format' : 'json',
                'nojsoncallback' : 1,
                'text' : 'Flickr',
                'extras' : "date_upload",
                }
        url = "http://api.flickr.com/services/rest/?%s"%(urllib.urlencode(args))
        
        flickr_photos = eval(urllib.urlopen(url).readline())
        template = "http://farm%s.static.flickr.com/%s/%s_%s.jpg"
        photos = []
        
        for photo in flickr_photos["photos"]["photo"]:
            photos.append(template%(photo["farm"], photo["server"],
                                    photo["id"], photo["secret"]))
            

        return photos

    def flickr(self):
        self.word_ = self.request.get('query')
        if self.word_ is not None:
            self.word_ = self.word_.encode('utf-8')
            args = {'method' : 'flickr.photos.search',
                    'api_key' : '58abc315168ff0008467f003e2d28b04',
                    'per_page' : '50',
                    'sort' : 'date-posted-desc',
                    'format' : 'json',
                    'nojsoncallback' : 1,
                    'text' : self.word_,
                    'extras' : "date_upload",
                    }
            url = "http://api.flickr.com/services/rest/?%s"%(urllib.urlencode(args))
            
            flickr_photos = eval(urllib.urlopen(url).readline())
            template = "http://farm%s.static.flickr.com/%s/%s_%s.jpg"
            photos = []
            
            for photo in flickr_photos["photos"]["photo"]:
                photos.append(template%(photo["farm"], photo["server"],
                                        photo["id"], photo["secret"]))


            storage = FileStorage.FileStorage('init_photos.fs')
            db = DB(storage)
            connection = db.open()
            root = connection.root()
            arc = root['init']

            if len(photos) != 0:
                transaction.begin()
                arc.append(photos[0])
                root['init'] = arc
                transaction.commit()

            connection.close()
            db.close()

            return photos

        else:
            #return self.default()
            return self.arc()


    def getQuery(self):
        print 'a'



class FeedAdmin(Persistent, object):
    def __init__(self, url, updated):
        self.objectIds = []
        self.url = url
        self.updated = updated

    def getDate(self):
        return self.upadted

    def getUrl(self):
        return self.url


class getFeed(grok.View):
    import feedparser, datetime, re
    
    def todate(self, st):
        if(str is None):
            return str(self.datetime.date.today())
        
        day_list = []
        day_temp = st.split('-')
        for d in day_temp:
            day_list.append(int(d))

        day = day_list.pop()
        month = day_list.pop()
        year = day_list.pop()

        re_date = self.datetime.date(year, month, day)

        return re_date
    
    def getUrl2(self):
        storage = FileStorage.FileStorage('feed.fs')
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        new = self.getNew()
        urllist = []
        list = []

        list = root['Feed']

        if new is not None:
            list.append(FeedAdmin(new, self.datetime.date.today() - self.datetime.timedelta(7)))

        transaction.begin()
        root['Feed'] = list
        transaction.commit()

        feedlist = root['Feed']
        for f in feedlist:
            urllist.append([f.url, f.updated])

        connection.close()
        db.close()

        root['Feed'] = []

        return urllist

    def putFeed2(self, urllist):

        for u in urllist:
            print u
        print '\n'

        storage = FileStorage.FileStorage('feed.fs')
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        feedlist = []

        for list in urllist:
            feedlist.append(FeedAdmin(list[0], list[1]))

        transaction.begin()
        root['Feed'] = feedlist
        transaction.commit()

        connection.close()
        db.close()


    def getUrl(self):
        url = []
        list = open('/Users/daisuke/zope3/Flickr1/src/flickr1/subscription.txt', 'r+')

        for l in list:
            url.append(l.split(','))

        if self.getNew() is not None:
            url.append([self.getNew(), str(self.datetime.date.today())])

        for u in url:
            if len(u) == 1:
                u[0] = u[0][:-1]
                u.append(str(self.datetime.date.today()))
                
            else:
                u[1] = u[1][:-1]

        list.close()
        
        return url


    def feed(self):
        urllist = []
        urllist = self.getUrl2()
    
        result = []
        r = self.re.compile('\d\d\d\d-\d\d-\d\d$')
        for url in urllist:
            p = self.feedparser.parse(url[0])
            feeddate = []
            lastday = url[1]
            #lastday = self.todate(url[1])
            count = 0
            for entry in p.entries:
                if r.match(entry["updated"]):
                    # change as 'datetime' format
                    updated_date = self.todate(entry["updated"])
                else:
                    updated_date = self.todate(entry["updated"][:10])
                # comparing each date
                if lastday < updated_date:
                    result.append(entry)
                    if count == 0:
                        url[1] = updated_date
                        #url[1] = str(updated_date)
                        count += 1

        self.putFeed2(urllist)

        return result

    def getNew(self):
        new = self.request.get('new')
        if new is not None:
            return new
        else:
            return None



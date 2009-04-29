# -*- coding: utf-8; -*-

import urllib

name = u'香里奈'
name = name.encode('utf-8')

args = {'method' : 'flickr.photos.search',
        'api_key' : '58abc315168ff0008467f003e2d28b04',
        'per_page' : '1',
        'sort' : 'date-posted-desc',
        'format' : 'json',
        'nojsoncallback' : 1,
        'text' : name,
        'extras' : "date_upload",
        }
url = "http://api.flickr.com/services/rest/?%s"%(urllib.urlencode(args))

flickr_photos = eval(urllib.urlopen(url).readline())
template = "http://farm%s.static.flickr.com/%s/%s_%s.jpg"
photos = []

for photo in flickr_photos["photos"]["photo"]:
    photos.append(template%(photo["farm"], photo["server"], photo["id"], photo["secret"]))

print photos
    
    

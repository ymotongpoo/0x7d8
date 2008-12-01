# -*- encoding: utf-8 -*-
"""
WSSE.py

WSSEAtomClinet:
    http://d.hatena.ne.jp/keyword/%A4%CF%A4%C6%A4%CA%A5%D5%A5%A9%A5%C8%A5%E9%A5%A4%A5%D5AtomAPI?kid=88110
    http://d.hatena.ne.jp/kenkitii/20060429/p1
"""

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2008/11/27 09:44:52$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import random, datetime, time
import base64, sha
import urllib,httplib
from xml.dom import minidom

class WSSEAtomClient:
    def __init__(self, userid='', password=''):
        self.userid = userid
        self.password = password
        self.useragent = 'WSSEAtomClient'
        self.wsse = None


    def createHeaderToken(self):
        nonce = sha.sha(str(time.time() + random.random())).digest()
        nonce64 = base64.encodestring(nonce).strip()

        created = datetime.datetime.now().isoformat() + 'Z'

        passdigest = sha.sha(nonce + created + self.password).digest()
        pass64 = base64.encodestring(passdigest).strip()

        wsse = 'UsernameToken Username="%(u)s", PasswordDigest="%(p)s", Nonce="%(n)s", Created="%(c)s"'
        value = dict(u = self.userid, p = pass64, n = nonce64, c = created)

        self.wsse = wsse % value


    def atomRequest(self, method, endpoint, body, content_type):
        header_info = {'X-WSSE': self.wsse,
                       'Content-Type': content_type,
                       'Authorization': 'WSSE profile="UsernameToken"',
                       'User-Agent': self.useragent}
        
        conninfo = urllib.splittype(endpoint)
        conntypeinfo = conninfo[0]
        connhostinfo = urllib.splithost(conninfo[1])
        
        conn = httplib.HTTPConnection(connhostinfo[0])
        conn.request(method, connhostinfo[1], body, header_info)
        r = conn.getresponse()
        """
        if r.status != 200:
            raise Exception('login failure')
        """
        response = dict(status = r.status,
                        reason = r.reason,
                        data = r.read())
        conn.close()
        return response


    def getCollection(self, data):
        element_hierarchy = ['workspace', 'collection']
        doc = minidom.parseString(data).getElementsByTagName('workspace').item(0)
        
        service = []
        for n in doc.getElementsByTagName('collection'):
            url = n.getAttribute('href')
            title = n.getElementsByTagName('atom:title').item(0).childNodes[0].data
            service.append(
                dict(url = url,
                     title = title)
                )
        
        return service


class MixiClient(WSSEAtomClient):
    def __init__(self, userid, password):
        WSSEAtomClient.__init__(self, userid, password)

    def __getService(self, endpoint, body='', content_type='text/xml'):
        self.createHeaderToken()        
        r = self.atomRequest('GET', endpoint, body, content_type)
        return r

    def __postService(self, endpoint, body, content_type='text/xml'):
        self.createHeaderToken()
        r = self.atomRequest('POST', endpoint, body, content_type)
        return r

    def __createSenderXML(self, elem_dict):
        impl = minidom.getDOMImplementation()
        doc = impl.createDocument(None, 'entry', None)

        header = doc.documentElement
        header.attributes['xmlns'] = 'http://www.w3.org/2005/Atom'
        header.attributes['xmlns:app'] = 'http://www.w3.org/2005/app#'

        for k, v in elem_dict.iteritems():
            elem = doc.createElement(k)
            elem.appendChild(doc.createTextNode(v))
            header.appendChild(elem)

        body = doc.toxml(encoding='UTF-8')
        doc.unlink()
            
        return body


    def getTracks(self):
        d = self.__getService('http://mixi.jp/atom/tracks')
        service = self.getCollection(d['data'])[0]['url']

        d = self.atomRequest('GET',service,'')
        doc = minidom.parseString(d['data'])
        
        tracks = []
        for n in doc.getElementsByTagName('entry'):
            link = n.getElementsByTagName('link').item(0).getAttribute('href')
            person = n.getElementsByTagName('author').item(0)
            name = person.getElementsByTagName('name').item(0).childNodes[0].data
            updated = n.getElementsByTagName('updated').item(0).childNodes[0].data
            
            tracks.append(
                dict(name = name,
                     link = link,
                     updated = updated)
                )
        
        return tracks


    def getNotify(self):
        d = self.__getService('http://mixi.jp/atom/notify')
        service = self.getCollection(d['data'])[0]['url']

        d = self.__getService(service)
        doc = minidom.parseString(d['data'])
        
        notify = []
        for n in doc.getElementsByTagName('entry'):
            link = n.getElementsByTagName('link').item(0).getAttribute('href')
            title = n.getElementsByTagName('title').item(0).childNodes[0].data
            updated = n.getElementsByTagName('updated').item(0).childNodes[0].data
            
            notify.append(
                dict(title = title,
                     link = link,
                     updated = updated)
                )
        
        return notify


    def getFriends(self):
        d = self.__getService('http://mixi.jp/atom/friends')
        service = self.getCollection(d['data'])[0]['url']

        d = self.__getService(service)
        doc = minidom.parseString(d['data'])
        
        friends = []
        for n in doc.getElementsByTagName('entry'):
            link = n.getElementsByTagName('link').item(0).getAttribute('href')
            name = n.getElementsByTagName('title').item(0).childNodes[0].data
            updated = n.getElementsByTagName('updated').item(0).childNodes[0].data

            group = []
            for item in n.getElementsByTagName('category'):
                group.append(item.getAttribute('label'))
            
            friends.append(
                dict(name = name,
                     link = link,
                     updated = updated,
                     group = group)
                )
        return friends

    
    def getUpdates(self):
        """
        something is wrong with 'uri' element.
        """
        d = self.__getService('http://mixi.jp/atom/updates')
        service = self.getCollection(d['data'])[0]['url']

        d = self.__getService(service)
        doc = minidom.parseString(d['data'])
        
        updates = []
        for n in doc.getElementsByTagName('entry'):
            link = n.getElementsByTagName('link').item(0).getAttribute('href')
            title = n.getElementsByTagName('title').item(0).childNodes[0].data
            updated = n.getElementsByTagName('updated').item(0).childNodes[0].data
            label = n.getElementsByTagName('category').item(0).getAttribute('label')
            author = n.getElementsByTagName('author').item(0)
            name = author.getElementsByTagName('name').item(0).childNodes.item(0).data
            #uri = author.getElementsByTagName('uri').item(0).childNodes.item(0).data
            
            updates.append(
                dict(name = name,
                     #uri = uri,
                     title = title,
                     link = link,
                     updated = updated,
                     label = label)
                )
        return updates
        

    def getPhotoService(self):
        d = self.__getService('http://photo.mixi.jp/atom/r=3')
        service = self.getCollection(d['data'])
        return service


    def createAlbum(self, title, summary):
        for s in self.getPhotoService():
            if s['title'] == 'photo album':
                url = s['url']

        elem_dict = dict(title = title,
                         summary = summary,
                         content = '')
        body = self.__createSenderXML(elem_dict)
        d = self.__postService(url, body)

        doc = minidom.parseString(d['data'])
        source = doc.getElementsByTagName('entry').item(0).\
                 getElementsByTagName('id').item(0).childNodes[0].data
        chop = source.split('/')
        endpoint = url + '/' + chop[len(chop)-1]
        
        return endpoint


    def postPicsToAlbum(self, pics, url):
        for pic in pics:
            try:
                p = open(pic, 'rb').read()
                d = self.__postService(url, p, 'image/jpeg')
            except Exception, e:
                print 'file -->', pic, ' caused failure', e
        return d


    def postDiary(self, title, summary, pic):
        """
        dict should be in this order
        """
        d = self.__getService('http://mixi.jp/atom/diary')
        service = self.getCollection(d['data'])[0]['url']
        pics = [pic]
        d = self.postPicsToAlbum(pics, service)

        # get edit uri
        edituri = ''
        doc = minidom.parseString(d['data'])
        urls = doc.getElementsByTagName('entry').item(0).getElementsByTagName('link')
        for l in urls:
            if 'edit' == l.getAttribute('rel'):
                edituri = l.getAttribute('href')

        if len(edituri) > 0:
            elem_dict = dict(summary = summary,
                             title = title)
                         
            body = self.__createSenderXML(elem_dict)
            d = self.__postService(edituri, body)
            return d
        elif len(edituri) == 0:
            raise 'URI Error'

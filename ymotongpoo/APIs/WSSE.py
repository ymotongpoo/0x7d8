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
import httplib
from xml.dom import minidom

class WSSEAtomClient:
    def __init__(self, userid='', password='', endpoint=''):
        self.userid = userid
        self.password = password
        self.endpoint = endpoint
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


    def atomRequest(self, method, URI, body):
        header_info = {'X-WSSE': self.wsse,
                       'Content-Type':'text/xml',
                       'Authorization': 'WSSE profile="UsernameToken"',
                       'User-Agent': self.useragent}
        conn = httplib.HTTPConnection(self.endpoint)
        conn.request(method, URI, body, header_info)
        r = conn.getresponse()
        if r.status != 200:
            raise Exception('login failure')
        response = dict(status = r.status,
                        reason = r.reason,
                        data = r.read())
        conn.close()
        return response


    def getCollection(self, data):
        element_hierarchy = ['workspace', 'collection']
        node = minidom.parseString(data)
        for v in element_hierarchy:
            node = node.getElementsByTagName(v)[0]
        service = node.getAttribute('href')
        print service



MIXI_ROOTENDPOINT = 'mixi.jp'

class MixiClient(WSSEAtomClient):
    def __init__(self, userid, password):
        WSSEAtomClient.__init__(self, userid, password)
        self.endpoint = MIXI_ROOTENDPOINT


    def __getService(self, surl, r, member_id, endpoint=''):
        if len(endpoint) > 0:
            self.endpoint = endpoint
        self.createHeaderToken()
        
        d = dict(r = r, member_id = member_id)
        l = ['']
        for k, v in d.iteritems():
            l.append(k + '=' + str(v))
        url = surl + '/'.join(l)
        r = self.atomRequest('GET', url, '')
        return r


    def getTracks(self, r, member_id):
        d = self.__getService('/atom/tracks', r, member_id)
        doc = minidom.parseString(d['data'])

        tracks = []
        for n in doc.getElementsByTagName('entry'):
            link = n.getElementsByTagName('link').item(0).getAttribute('href')
            person = n.getElementsByTagName('author').item(0)
            name = person.getElementsByTagName('name').item(0).childNodes[0].data
            updated = n.getElementsByTagName('updated').item(0).childNodes[0].data
            
            tracks.append(dict(name = name, link = link, updated = updated))
        
        return tracks


    def getNotify(self, r, member_id):
        d = self.__getService('/atom/notify', r, member_id)
        doc = minidom.parseString(d['data'])
        
        notify = []
        for n in doc.getElementsByTagName('entry'):
            link = n.getElementsByTagName('link').item(0).getAttribute('href')
            title = n.getElementsByTagName('title').item(0).childNodes[0].data
            updated = n.getElementsByTagName('updated').item(0).childNodes[0].data
            
            notify.append(dict(title = title, link = link, updated = updated))
        
        return notify


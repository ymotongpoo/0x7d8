# -*- encoding: utf-8 -*-
"""
Haiku.py

Based on Twitter API
    http://watcher.moe-nifty.com/memo/docs/twitterAPI13.txt
"""

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2008/11/22 09:57:30$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import urllib
import urllib2

FORMAT = set(['xml', 'rss', 'json', 'atom'])
default_format = 'json'

class Twitter:
    def __init__(self, username, password, base_url='', proxy_host='', proxy_port=''):
        self.username = username
        self.password = password
        self.base_url = base_url if len(base_url) > 0 else 'http://twitter.com/'
        
        if len(proxy_host) > 0 and type(proxy) is IntType:
            self.proxies = {'http': proxy_host + ':' + proxy_port}
        else:
            self.proxies = {}

        if 'http' in self.proxies:
            auth_handler = urllib2.ProxyBasicAuthHandler()
        else:
            auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password('Twitter API', base_url, self.username, self.password)
        self.opener = urllib2.build_opener(auth_handler)
        urllib2.install_opener(self.opener)

    def __add_format(url, format):
        if format in FORMAT:
            url = url + '.' + format
        else:
            url = url + '.' + default_format
        return url

    def __open_url_in_get(self, url, get_dict={}):
        if len(get_dict) > 0:
            params = urllib.urlencode(get_dict)
            f = urllib2.urlopen(url + '?' + params)
        else:
            f = urllib2.urlopen(url)
        return f.read()

    def __open_url_in_post(self, url, post_dict={}):
        if len(post_dict) > 0:
            params = urllib.urlencode(post_dict)
            f = urllib2.urlopen(url, params)
            return f.read()
        else:
            return

    def __query_dict_generator(self, func_args):
        get_dict = {}
        if 'since_id' in func_args and func_args['since_id'] > 0 and type(func_args['since_id']) is int:
            get_dict['since_id'] = func_args['since_id']
        if 'twitter_id' in func_args and len(func_args['twitter_id']) > 0:
            get_dict['twitter_id'] = func_args['twitter_id']
        if 'since' in func_args and len(func_args['since']) > 0:
            get_dict['since'] = func_args['since']
        if 'page' in func_args and func_args['page'] > 0 and type(func_args['page']) is int:
            get_dict['page'] = func_args['page']
        if 'lite' in func_args and not func_args['lite']:
            get_dict['lite'] = 'true'
        return get_dict    

    def __get_request_without_options(self, url_part, format):
        url = self.base_url + url_part
        url = self.__add_format(url, format)
        d = self.__open_url_in_get(url)
        return d

    def __get_request_with_options(self, url_part, format, dict):
        url = self.base_url + url_part
        url = self.__add_format(url, format)
        get_dict = self.__query_dict_generator(dict)
        d = self.__open_url_in_get(url, get_dict)
        return d

    def PublicTimeline(self, format=default_format, since_id=-1):
        return self.__get_request_with_options('statuses/public_timeline', format, locals())

    def friendsTimeline(self, format=default_format, twitterid='', since='', page=1):
        """
        since -- expects same type as the return of strftime()
        """
        url_part = 'statuses/friends_timeline'
        if len(twitterid) > 0:
            url_part = url_part + '/' + twitterid
        return self.__get_request_with_options(url_part, format, locals())

    def userTimeline(self, format=default_format, twitterid='', count=20, since='', since_id='', page=1):
        """
        since -- expects same type as the return of strftime()
        """
        url_part = 'statuses/user_timeline'
        if len(twitterid) > 0:
            url_part = url_part + '/' + twitterid            
        return self.__get_request_with_options(url_part, format, locals())
        

    def showStatusByID(self, format=default_format, status_id):
        return self.__get_request_without_options('statuses/show/' + status_id, format)

    def updateStatus(self, format=default_format, status, source=''):
        url = self.base_url + 'statuses/update'
        url = self.__add_format(url, format)
        if len(status) =< 160:
            post_dict['status'] = status
        if len(source) > 0:
            post_dict['source'] = source
        d = self.__open_url_in_post(url, post_dict)
        return d

    def replies(self, format=default_format, since='', since_id='', page=1):
        return self.__get_request_with_options('statuses/replies', format, locals())

    def destroyPost(self, format=default_format, status_id):
        return self.__get_request_without_options('statuses/destroy/' + status_id, format)

    def friends(self, format=default_format, twitterid='', page=1, lite=False, since=''):
        return self.__get_request_with_options('statuses/friends', format, locals())

    def followers(self, format=default_format, twitterid='', page=1, lite=False):
        return self.__get_request_with_options('statuses/followers', format, locals())

    def featured(self, format=default_format):
        return self.__get_request_without_options('statuses/featured', format)

    def showUserInfo(self, format=default_format, twitterid, email=''):
        url = self.base_url + 'users/show'
        if 'email' in locals():
            url = self.__add_format(url, format)
            get_dist['email'] = email
        else:
            url = url + '/' + twitterid
            url = self.__add_format(url, format)
            get_dict = self.__query_dict_generator(locals())
        d = self.__open_url_in_get(url, get_dict))
        return d

    def directMsgs(self, formaat=default_format, since='', since_id='', page=1):
        return self.__get_request_with_options('direct_messages', format, locals())

    def sentMsgs(self, format=default_format, since='', since_id='', page=1):
        return self.__get_request_with_options('direct_messages/sent', format, locals())
    
    def sendNewDirectMsg(self, format=default_format, user, text):
        url = self.base_url + 'direct_messages/new'
        url = self.__add_format(url, format)
        post_dict = self.__query_dict_generator(locals())
        d = self.__open_url_in_post(url, post_dict)
        return d

    def destroyDirectMsg(self, format=default_format, msgid):
        url = self.base_url + 'direct_messages/destroy/'
        url = self.__add_format(url, format)
        if type(msgid) is int:
            get_dict['id'] = msgid
            d = self.__open_url_in_get(url, get_dict)
            return d
        else:
            return
    
    def createFriend(self, format=default_format, twitterid):
        return self.__get_request_without_options('friendships/create/' + twitterid, format)

    def destroyFriend(self, format=default_format, twitterid):
        return self.__get_request_without_options('friendships/destroy/' + twitterid, format)

    def existsRelationship(self, format=default_format, user_a, user_b):
        url = self.base_url + 'friendships/exists'
        url = self.__add_format(url, format)
        get_dict['user_a'] = user_a
        get_dict['user_b'] = user_b
        d = self.__open_url_in_get(url, get_dict)
        return d
           
    def verifyCredentials(self, format=default_format):
        url = self.base_url + 'account/verify_credentials'
        url = self.__add_format(url, format)
        d = self.__open_url_in_get(url)
        return d

    def endSession(self):
        url = self.base_url + 'account/end_session'
        d = self.__open_url_in_get(url)
        return d

    def archivePost(self, format=default_format, page=1, since='', since_id=''):
        return self.__get_request_with_options('account/archive', format, locals())

    def updateLocation(self, format=default_format, location):
        url = self.base_url + 'account/update_location'
        url = self.__add_format(url, format)
        get_dict['location'] = location
        d = self.__open_url_in_get(url, get_dict)
        return d

    def updateDeliveryDevice(self, format=default_format, device):
        devices = set(['sms', 'im', 'none'])
        url = self.base_url + 'account/update_delivery_device'

        post_dict = self.__query_dict_generator(locals())
        d = self.__open_url_in_post(url, post_dict)
        return d

    def rateLimitStatus(self, format=default_format):
        return self.__get_request_without_options('account/rate_limit_status', format)

    def favoritesPost(self, format=default_format, twitterid='', page=1):
        return self.__get_request_with_options('favorites', format, locals())

    def createFavorite(self, format=default_format, twitterid):
        return self.__get_request_without_options('favourings/create/' + twitterid, format)

    def destroyFavorite(self, format=destroyFavorite, twitterid):
        return self.__get_request_without_options('favourings/destory/' + twitterid, format)

    def followIM(self, format=default_format, twitterid):
        return self.__get_request_without_options('notifications/follow/' + twitterid, format)

    def leaveIM(self, format=default_format, twitterid):
        return self.__get_request_without_options('notifications/leave/' + twitterid, format)

    def createBlock(self, format=default_format, twitterid):
        return self.__get_request_without_options('blocks/create/' + twitterid, format)

    def destoryBlock(self, format=default_format, twitterid):
        return self.__get_request_without_options('blocks/destroy/' + twitterid, format)

    def testConnection(self, format=default_format):
        return self.__get_request_without_options('help/test', format)

    def downtimeSchedule(self, format=default_format):
        return self.__get_request_without_options('help/downtime_schedule', format)

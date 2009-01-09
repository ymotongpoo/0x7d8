#!/usr/bin/python

import urllib2
import urllib
import feedparser
import json
import random
import string
import sys

def userslist(url):
    users = []
        
    try:
        re = urllib2.urlopen('http://b.hatena.ne.jp/entry/json/' + url)
    except:
        return users

    tmp = re.next()
    if tmp == '(null)':
        return users

    tmp = string.replace(tmp, '(', '[')
    tmp = string.replace(tmp, ')', ']')

    info = json.JsonReader().read(tmp)
    users = [u['user'] for u in info[0]['bookmarks'] if u['user'] != []]
    if not users:
        users = []

    return users
        
def getuserlist(user=None):
    ERROR_CODE = 'user not found'
    favorite_list = []

    favorites_users_json = 'http://s.hatena.ne.jp/' + user + '/favorites.json'

    try:
        re = urllib2.urlopen(favorites_users_json)
    except:
        print ERROR_CODE
        return favorite_list
    
    users_favorites = json.JsonReader().read(re.next())
    
    for usr in users_favorites['favorites']:
        favorite_list.append(usr['name'])
                    
    return favorite_list


def getpageinfo(users_list=None):
    links = []
    link = {}

    for name in random.sample(users_list, 3):
        us = ''
        for n in name[:2]:
            us += n

        b_url = 'http://b.hatena.ne.jp/' + name + '/rss'
        feed = feedparser.parse(b_url)
        
            
        for f in feed.entries[:5]:
            """
            users = self.userslist(f['links'][0]['href'])
            if name in users:
            continue
            """

            link['link'] = f['links'][0]['href']
            link['title'] = f['title']
            link['comment'] = f['summary_detail']['value']
            link['author'] = f['author']
            link['favicon'] = 'http://www.hatena.ne.jp/users/' + us + '/' + f['author'] + '/profile_s.gif'
            
            links.append(link)
            link = {}
    return links


def main(user=None):
    links = []
    link = {}

    users_list = getuserlist(user)
    if not users_list:
        return

    links = getpageinfo(users_list)

    print links[0]

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print 'usage: python HatenaFavorites.py [username] '
    

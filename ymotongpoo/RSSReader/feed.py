# -*- encoding: utf-8 -*-;
"""
feed.py

Class for parsing RSS/ATOM feeds.
Referred to Ch.8.5.3 in Python Library Referrence
"""

from xml.parsers import expat

class FeedParser:
    def __init__(self, body, feedtype):
        self.body = body
        self.feedtype = feedtype
        parser = xml.parsers.expat.ParserCreate()

    def start_element(self, name, attrs):
        print 'Start element: ', name, attrs

    def end_element(self, name):
        print 'End element: ', name

    def char_data(data):
        print 'Character data: ', repr(data)

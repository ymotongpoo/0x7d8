'''
Created on 2009/04/27

@author: ymotongpoo
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('summary.views',
    url(r'^updated/(\d+)/$', 'updated', name='updated'),
    url(r'^hot/(\d+)/$', 'hot', name='hot'),
    url(r'^user/(\d+)/$', 'user', name='user'),
    url(r'^.*', 'index', name='index'),
)
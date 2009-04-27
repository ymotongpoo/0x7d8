# coding: utf-8
'''
Created on 2009/04/27

@author: ymotongpoo
'''
# Create your views here.
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from models import Site, Entry

def index(request):
    entries = Entry.objects.all().order_by('-posted')
    return render_to_response('index.html',
                              {'entries':entries})

def updated(request, offset):
    pass

def hot(request, offset):
    pass

def user(request, offset):
    pass

'''
Created on 2009/04/27

@author: ymotongpoo
'''
from django.contrib import admin
from models import *

class SiteAdmin(admin.ModelAdmin):
    pass

class EntryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Site, SiteAdmin)
admin.site.register(Entry, EntryAdmin)

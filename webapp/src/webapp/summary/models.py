# coding:utf-8
from django.db import models
from datetime import datetime

# Create your models here.

class Site(models.Model):
    '''
    まとめサイト
    '''
    title = models.CharField(u'サイトタイトル', max_length=255)
    url = models.URLField(u'サイトURL', verify_exists=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        db_table = 'tsite'
        verbose_name = u'サイト'
        verbose_name_plural = u'サイト'
        
class Entry(models.Model):
    '''
    まとめ記事
    '''
    title = models.TextField(u'エントリタイトル', max_length=1000)
    url = models.URLField(u'エントリURL')
    huser = models.PositiveIntegerField(u'はてブ数', null=True, blank=True)
    duser = models.PositiveIntegerField(u'delicious数', null=True, blank=True)
    buser = models.PositiveIntegerField(u'Buzzurl数', null=True, blank=True)
    posted = models.DateTimeField(u'投稿日時', default=datetime.now)
    site_id = models.ForeignKey(Site)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        db_table = 'tentry'
        ordering = ['-posted']
        verbose_name = u'エントリ'
        verbose_name_plural = u'エントリ'
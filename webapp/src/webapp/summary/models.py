from django.db import models
from datetime import datetime

# Create your models here.

class Site(models.Model):
    title = models.CharField(u'サイトタイトル', max_length=255)
    url = models.URLField(u'サイトURL', verify_exists=True)
    class Meta:
        db_table = 'tsite'
        verbose_name = u'サイト'
        verbose_name_plural = u'サイト'
        
class Entry(models.Model):
    title = models.TextField(u'エントリタイトル', max_length=1000)
    url = models.URLField(u'エントリURL')
    huser = models.PositiveIntegerField(u'はてブ数')
    duser = models.PositiveIntegerField(u'delicious数')
    buser = models.PositiveIntegerField(u'Buzzurl数')
    posted = models.DateTimeField(u'投稿日時', default=datetime.now)
    site_id = models.ForeignKey(Site)
    class Meta:
        db_table = 'tentry'
        ordering = ['-posted']
        verbose_name = u'エントリ'
        verbose_name = u'エントリ'
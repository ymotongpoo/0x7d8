from django.db import models
from datetime import datetime

# Create your models here.

class Site(models.Model):
    title = models.CharField(u'�T�C�g�^�C�g��', max_length=255)
    url = models.URLField(u'�T�C�gURL', verify_exists=True)
    class Meta:
        db_table = 'tsite'
        verbose_name = u'�T�C�g'
        verbose_name_plural = u'�T�C�g'
        
class Entry(models.Model):
    title = models.TextField(u'�G���g���^�C�g��', max_length=1000)
    url = models.URLField(u'�G���g��URL')
    huser = models.PositiveIntegerField(u'�͂ău��')
    duser = models.PositiveIntegerField(u'delicious��')
    buser = models.PositiveIntegerField(u'Buzzurl��')
    posted = models.DateTimeField(u'���e����', default=datetime.now)
    site_id = models.ForeignKey(Site)
    class Meta:
        db_table = 'tentry'
        ordering = ['-posted']
        verbose_name = u'�G���g��'
        verbose_name = u'�G���g��'
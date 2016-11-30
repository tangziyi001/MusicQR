from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

class Music(models.Model):
    artist = models.ForeignKey(
        Artist,
        on_delete = models.CASCADE,
        verbose_name = 'the composer'
    )
    title = models.CharField(max_length=40)
    genre = models.CharField(max_length=40)
    date = models.DateField()
    rate = models.IntegerField()
    def __str__(self):
        return self.title



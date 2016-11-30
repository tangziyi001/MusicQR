from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Music(models.Model):
    title = models.CharField(max_length=40)
    genre = models.CharField(max_length=40) 
    def __str__(self):
        return self.title
class Artist(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

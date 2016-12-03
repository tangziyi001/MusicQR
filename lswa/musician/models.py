from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    nationality = models.CharField(max_length=40)

class Music(models.Model):
    artist = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        verbose_name = 'the composer'
    )
    title = models.CharField(max_length=40)
    genre = models.CharField(max_length=40)
    date = models.DateField(auto_now_add=True)
    rate = models.IntegerField()
    download_url = models.CharField(max_length=1000)
    def __str__(self):
        return self.title

class MusicQuery(models.Model):
    query = models.ForeignKey(
        Music,
        on_delete = models.CASCADE,
        verbose_name = 'arbitrary name'
    )
    token = models.CharField(max_length=1000)

class Download(models.Model):
    music = models.ForeignKey(
        Music,
        on_delete = models.CASCADE,
        verbose_name = 'downloaded music'
    )
    download_time = models.DateTimeField(auto_now=True)
    download_loc = models.CharField(max_length=100)


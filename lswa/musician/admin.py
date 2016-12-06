from django.contrib import admin
from django.contrib.auth.models import User
from .models import Artist, Music, Download, MusicQuery
# Register your models here.
admin.site.register(Artist)
admin.site.register(Music)
admin.site.register(Download)
admin.site.register(MusicQuery)

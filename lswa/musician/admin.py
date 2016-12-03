from django.contrib import admin
from django.contrib.auth.models import User
from .models import Artist
from .models import Music
from .models import Download
# Register your models here.
admin.site.register(Artist)
admin.site.register(Music)
admin.site.register(Download)

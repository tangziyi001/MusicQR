from django.conf.urls import url

from . import views
app_name = 'musician'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^download/$', views.download, name='download'),
    url(r'^login/$', views.artist_login, name='artist_login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^artist/(?P<artist_id>[a-zA-Z0-9]+)/$', views.artist, name='artist'),
    url(r'^statistics/(?P<artist_id>[a-zA-Z0-9]+)/(?P<music_id>[0-9]+)/$', views.artist, name='statistics'),
    url(r'^logout/$', views.artist_logout, name='artist_logout'),
    url(r'^getQRCode/(?P<music_id>[0-9]+)/$', views.getQRCode, name='get_QR'),
    url(r'^download/(?P<token>[a-zA-Z0-9.]+)/$', views.download, name='download_file'),
    url(r'^music/(?P<token>[a-zA-Z0-9]+)/$', views.music_query, name='music_query'),
    url(r'^downloadQR/$', views.downloadQR, name='download_file'),
]

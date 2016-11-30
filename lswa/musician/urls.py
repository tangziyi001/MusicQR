from django.conf.urls import url

from . import views
app_name = 'musician'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^download/$', views.download, name='download'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^artist/(?P<artist_id>[0-9]+)/$', views.artist, name='artist'),
    url(r'^statistics/(?P<artist_id>[0-9]+)/$', views.artist, name='statistics'),
]

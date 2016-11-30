from django.conf.urls import url

from . import views
app_name = 'musician'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^artist/(?P<artist_id>[0-9]+)/$', views.artist, name='artist'),
]

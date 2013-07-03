
from django.conf.urls.defaults import patterns, url

from wcdb import views

urlpatterns = patterns('',
	url(r'^$', views.index)
)

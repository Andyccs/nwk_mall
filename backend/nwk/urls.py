from django.conf.urls import patterns, url
from nwk import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='detail'),
)
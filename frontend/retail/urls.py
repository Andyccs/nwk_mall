from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'retail.views.home', name='home'),
)

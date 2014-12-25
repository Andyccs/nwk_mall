from django.conf.urls import patterns, include, url
from django.contrib import admin
import retail

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'shopgrab.views.home', name='home'),
    url(r'^$', 'shopgrab.views.about', name='about'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^retail/', retail.views.home,
        # name='home'),
    url(r'^retail/', include('retail.urls', namespace='retail')),
    # url(r'^login/$', include('login.urls', namespace='login')),
    # url(r'^logout/$', include('logout.urls', namespace='logout')),
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',
                       ('^$', RedirectView.as_view(url='wijn')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^wijn/', include('wijn.urls')),
)

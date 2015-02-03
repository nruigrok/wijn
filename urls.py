from django.conf.urls import patterns, url

from wijn import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)

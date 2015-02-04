from django.conf.urls import patterns, url

from wijn import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^subregio/(?P<regio>[\w -]+)$', views.subregio, name='subregio'),
    url(r'^subregio$', views.regiokiezer, name='regiokiezer'),
    url(r'^kleurperregio',views.kleurperregio, name='kleurperregio'),
    url(r'^regio$', views.regio, name='regio'),
    url(r'^kleur$', views.kleur, name='kleur'),
    url(r'^kleur/(?P<regio>[\w -]+)$', views.kleur, name='kleur'),
    url(r'^scores$', views.scores, name='scores'),
)

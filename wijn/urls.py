from django.conf.urls import patterns, url

from wijn import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^subregio/(?P<regio>[\w -]+)$', views.subregio, name='subregio'),
    url(r'^subregio$', views.regiokiezer, {'next': 'subregio'}, name='regiokiezer-subregio'),
    url(r'^kleurmeerkeuze/(?P<regio>[\w -]+)$', views.kleurmeerkeuze, name='kleurmeerkeuze'),
    url(r'^kleurmeerkeuze$', views.regiokiezer, {'next' : 'kleurmeerkeuze'}, name='regiokiezer-kleurmeerkeuze'),
    url(r'^kleurperregio',views.kleurperregio, name='kleurperregio'),
    url(r'^regio$', views.regio, name='regio'),
    url(r'^druiven/(?P<regio>[\w -]+)$', views.druiven, name='druiven'),
    url(r'^druiven$', views.regiokiezer, {'next': 'druiven'}, name='regiokiezer-druiven'),
    url(r'^kleur$', views.kleur, name='kleur'),
    url(r'^kleur/(?P<regio>[\w -]+)$', views.kleur, name='kleur'),
    url(r'^scores$', views.scores, name='scores'),


                       
    url(r'^subregios2$', views.landenkiezer, {'next': 'subregios2'}, name='landenkiezer-subregios2'),
    url(r'^subregios2/(?P<land>[\w -]+)$', views.subregios2, name='subregios2'),
)

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
    url(r'^subregios2/(?P<land>[\w -]+)$', views.Subregios2View.as_view(), name='subregios2'),

    url(r'^streekdruiven$', views.landenkiezer, {'next': 'streekdruiven'}, name='landenkiezer-streekdruiven'),
    url(r'^streekdruiven/(?P<land>[\w -]+)$', views.StreekDruifView.as_view(), name='streekdruiven'),

    url(r'^streekdruivenmakkelijk$', views.landenkiezer, {'next': 'streekdruiven-makkelijk'}, name='landenkiezer-streekdruiven-makkelijk'),
    url(r'^streekdruivenmakkelijk/(?P<land>[\w -]+)$', views.StreekDruifMakkelijkView.as_view(), name='streekdruiven-makkelijk'),
                       
    url(r'^gemeentes$', views.landenkiezer, {'next': 'gemeentes'}, name='landenkiezer-gemeentes'),
    url(r'^gemeentes/(?P<land>[\w -]+)$', views.GemeenteView.as_view(), name='gemeentes'),

    url(r'^appellations$', views.landenkiezer, {'next': 'appellations'}, name='landenkiezer-appellations'),
    url(r'^appellations/(?P<land>[\w -]+)$', views.AppellationView.as_view(), name='appellations'),


    url(r'^docg$', views.landenkiezer, {'next': 'docg'}, name='landenkiezer-docg'),
    url(r'^docg/(?P<land>[\w -]+)$', views.DOCGView.as_view(), name='docg'),

    url(r'^docgdruif$', views.landenkiezer, {'next': 'docgdruif'}, name='landenkiezer-docgdruif'),
    url(r'^docgdruif/(?P<land>[\w -]+)$', views.DOCGDruifView.as_view(), name='docgdruif'),
    url(r'^docgdruifmakkelijk$', views.landenkiezer, {'next': 'docgdruif-makkelijk'}, name='landenkiezer-docgdruif-makkelijk'),
    url(r'^docgdruifmakkelijk/(?P<land>[\w -]+)$', views.DOCGDruifMakkelijkView.as_view(), name='docgdruif-makkelijk'),

    url(r'^vragen$', views.landenkiezer, {'next': 'vragen'}, name='landenkiezer-vragen'),                    
    url(r'^vragen/(?P<land>[\w -]+)$', views.VragenView.as_view(), name='vragen'),

)

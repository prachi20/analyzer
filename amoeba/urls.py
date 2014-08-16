from django.conf.urls import patterns, url
from amoeba import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'), url(r'^genes/$', views.genes, name='genes'), url(r'^plotProfile/$', views.plotProfile,name='plotProfile'))
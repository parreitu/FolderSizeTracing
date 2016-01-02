from django.conf.urls import patterns, url
from FolderSizeTracing import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'piechart.html', views.piechart, name='piechart'),
)
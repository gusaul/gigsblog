from django.conf.urls import patterns, include, url
from django.contrib import admin
import urls
from apps.blog import views

urlpatterns = patterns('',
    url(r'^p/(?P<pk>[\w\d]+)/(?P<slug>[\w\d-]+)/$', views.PostDetail.as_view(), name='detail'),
    url(r'^category/(?P<catname>[\w\d]+)/$', views.CatDetail.as_view(), name='catViews'),
    url(r'^tag/(?P<tagname>[\w\d]+)/$', views.TagDetail.as_view(), name='tagViews'),
)

from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
import urls
from apps.blog import views

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(pattern_name='admin')),
    url(r'^post/$', views.AdminPostList.as_view(), name='admin'),
    url(r'^post/add/', views.AddPost.as_view(), name='addPost'),
    url(r'^post/update/(?P<pk>[\w\d]+)/$', views.UpdatePost.as_view(), name='updatePost'),
    url(r'^post/delete/(?P<pk>[\w\d]+)/$', views.DeletePost.as_view(), name='deletePost'),
    url(r'^tag/$', views.TagView.as_view(), name='tag'),
    url(r'^tag/update/(?P<pk>[\w\d]+)/$', views.UpdateTag.as_view(), name='updateTag'),
    url(r'^tag/delete/(?P<pk>[\w\d]+)/$', views.DeleteTag.as_view(), name='deleteTag'),
    url(r'^category/$', views.CategoryView.as_view(), name='category'),
    url(r'^category/update/(?P<pk>[\w\d]+)/$', views.DeleteCategory.as_view(), name='deleteCategory'),
    url(r'^category/delete/(?P<pk>[\w\d]+)/$', views.UpdateCategory.as_view(), name='updateCategory'),
)
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .views import BlogSitemap

from . import views


urlpatterns = [
    # http: //localhost:8000/blog/1
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
    path('tag/<int:blog_tag_pk>', views.blog_with_tag, name='blogs_with_tag')
]

urlpatterns += [
    #sitemap
    path('sitemap.xml', sitemap, {'sitemaps': {'blog': BlogSitemap}}, name='django.contrib.sitemaps.views.sitemap')
]
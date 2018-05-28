"""djangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import home, login, register, login_for_medal
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.views import BlogSitemap

urlpatterns = [
    path('', home, name='home'),

    path('admin/', admin.site.urls),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('blog/', include('blog.urls')),
    path('login/', login, name='login'),
    path('login_for_medal/', login_for_medal, name='login_for_medal'),
    path('register/', register, name='register'),
    path('comment/', include('comment.urls')),
    path('likes/', include('likes.urls')),
    path('mdeditor/', include('mdeditor.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('search/', include('haystack.urls'))
]

urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)

urlpatterns += [
    #sitemap
    path('sitemap.xml', sitemap, {'sitemaps': {'blog': BlogSitemap}}, name='django.contrib.sitemaps.views.sitemap')
]

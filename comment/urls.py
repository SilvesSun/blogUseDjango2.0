from django.contrib import admin
from django.urls import path, include
from .views import update_comment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('update_comment', update_comment, name='update_comment'),

]
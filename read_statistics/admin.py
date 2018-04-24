from django.contrib import admin
from .models import ReadNum, ReadDetail


@admin.register(ReadNum)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['read_num', 'content_object']


@admin.register(ReadDetail)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['date' ,'read_num', 'content_object']
from django.contrib import admin
from .models import BlogType, Blog, Tag
from .forms import TagForm


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'overview', 'blog_type', 'author', 'get_read_num', 'created_time', 'updated_time', 'tags_list']
    filter_horizontal = ('tags',)
    list_display_links = ('id', 'title')
    list_filter = ('tags', 'created_time')  # 过滤器
    search_fields = ('title',)  # 搜索字段


@admin.register(Tag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ('id', 'name')





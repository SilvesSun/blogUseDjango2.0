import random

import mistune

from mistune import *
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, Page, PageNotAnInteger
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from blog.models import Blog, BlogType

from .models import Tag
from read_statistics.utils import read_statistics_once_read
from djangoBlog.forms import LoginForm
from django.contrib.sitemaps import Sitemap
from django.db.models import Q



class CustomerRender(mistune.Renderer):
    def block_code(self, code, lang=None):
        """Rendering block level code. ``pre > code``.

        :param code: text content of the code block.
        :param lang: language of the given code.
        """
        code = code.rstrip('\n')
        lang_dic = {
            'py': 'python',
            'js': 'javascript',
        }
        if not lang:
            code = escape(code, smart_amp=False)
            return '<pre><code>%s\n</code></pre>\n' % code
        code = escape(code, quote=True, smart_amp=False)
        return '<pre><code class="%s">%s\n</code></pre>\n' % (lang_dic.get(lang, lang), code)


def rand_blogs(except_id=0):
    rand_count = 5
    return Blog.objects.exclude(id=except_id).order_by('?')[:rand_count]


def get_blog_list_common(request, blogs_all_list):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(blogs_all_list, settings.DEFAULT_PAGE_NUMBER)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页码
    page_range = [i for i in range(max(current_page_num - 2, 1), min(current_page_num + 2, paginator.num_pages) + 1)]

    # 添加省略标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 添加首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    blog_types_list = BlogType.objects.annotate(blog_count=Count('blog'))

    # 获取日期归档对应的数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dic = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()

        blog_dates_dic[blog_date] = blog_count

    context = {'blogs': page_of_blogs.object_list,
               'page_of_blogs': page_of_blogs,
               'blogs_count': Blog.objects.count(),
               'blog_types': blog_types_list,
               'page_range': page_range,
               'blog_dates': blog_dates_dic}
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common(request, blogs_all_list)
    context['rand_blogs'] = rand_blogs()

    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    blog_content = mistune.markdown(blog.content)
    # blog_content = blog.content
    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['blog_content'] = blog_content
    context['login_form'] = LoginForm()
    response = render(request, 'blog/blog_detail.html', context) # 响应
    response.set_cookie(read_cookie_key, 'true') # 阅读cookie标记
    return response


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common(request, blogs_all_list)
    context['blog_type'] = blog_type
    context['rand_blogs'] = rand_blogs()
    return render(request, 'blog/blogs_with_type.html', context)


def blog_with_tag(request, blog_tag_pk):
    blog_tag = get_object_or_404(Tag, pk=blog_tag_pk)
    blogs_all_list = blog_tag.blog_set.all()
    context = get_blog_list_common(request, blogs_all_list)
    context['blog_type'] = blog_tag
    context['rand_blogs'] = rand_blogs()
    return render(request, 'blog/blogs_with_tag.html', context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year).filter(created_time__month=month)
    context = get_blog_list_common(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    context['rand_blogs'] = rand_blogs()
    return render(request, 'blog/blogs_with_date.html', context)


class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.updated_time

    def location(self, obj):
        return '/blog/%s' % obj.id


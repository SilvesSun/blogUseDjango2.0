from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, Page, PageNotAnInteger

from blog.models import Blog, BlogType
from django.conf import settings


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

    context = {'blogs': page_of_blogs.object_list,
               'page_of_blogs': page_of_blogs,
               'blogs_count': Blog.objects.count(),
               'blog_types': BlogType.objects.all(),
               'page_range': page_range,
               'blog_dates': Blog.objects.dates('created_time', 'month', order='DESC')}
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common(request, blogs_all_list)
    return render_to_response('blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    previous_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()
    next_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context = {'blog': blog,
               'previous_blog': previous_blog,
               'next_blog': next_blog}

    return render_to_response('blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year).filter(created_time__month=month)
    context = get_blog_list_common(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render_to_response('blog/blogs_with_date.html', context)

from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, Page, PageNotAnInteger

from blog.models import Blog, BlogType


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    page_num = request.GET.get('page', 1)
    pagenator = Paginator(blogs_all_list, 2)
    page_of_blogs = pagenator.get_page(page_num)

    context = {'blogs': page_of_blogs.object_list,
               'page_of_blogs': page_of_blogs,
               'blogs_count': Blog.objects.count(),
               'blog_types': BlogType.objects.all()}
    return render_to_response('blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {'blog': get_object_or_404(Blog, pk=blog_pk)}
    return render_to_response('blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blogs_with_type.html', context)



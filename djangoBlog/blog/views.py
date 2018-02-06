from django.shortcuts import render_to_response, get_object_or_404

from blog.models import Blog, BlogType


def blog_list(request):
    context = {'blogs': Blog.objects.all(),
               'blogs_count': Blog.objects.count()}
    return render_to_response('blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {'blog': get_object_or_404(Blog, pk=blog_pk)}
    return render_to_response('blog_detail.html', context)


def blogs_with_type(request, blogs_with_type):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blogs_with_type)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)



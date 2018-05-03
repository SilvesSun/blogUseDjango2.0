import datetime

from django.shortcuts import render_to_response, render, redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.cache import cache
from django.db.models import Sum, Count
from django.contrib import auth
from django.urls import reverse  # 反向解析
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


from blog.models import Blog, BlogType, Tag
from read_statistics.utils import *
from .forms import LoginForm, RegForm
from blog.views import rand_blogs


def get_seven_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:7]


def get_latest_blogs():
    return Blog.objects.all()[:10]


def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = get_seven_days_read_data(blog_content_type)
    blog_types_list = BlogType.objects.annotate(blog_count=Count('blog'))
    blog_tags_list = Tag.objects.annotate(blog_count=Count('blog'))

    # 获取缓存
    seven_days_hot_blogs = cache.get('seven_days_hot_blogs')
    if not seven_days_hot_blogs:
        seven_days_hot_blogs = get_seven_days_hot_blogs()
        cache.set('seven_days_hot_blogs', seven_days_hot_blogs, 60*60)

    lates_blogs = cache.get('latest_blogs')
    if not lates_blogs:
        lates_blogs = get_latest_blogs()
        cache.set('latest_blogs', lates_blogs, 60*60)

    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['seven_days_hot_date'] = get_seven_days_hot_blogs
    context['blog_types'] = blog_types_list
    context['blog_tags'] = blog_tags_list
    context['latest_blogs'] = lates_blogs
    context['blog_count'] = Blog.objects.all().count()
    context['rand_blogs'] = rand_blogs()

    return render(request, 'home.html', context)


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data.get('user')
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data.get('username')
            email = reg_form.cleaned_data.get('email')
            password = reg_form.cleaned_data.get('password')
            user = User.objects.create(username=username, email=email, password=make_password(password))
            user.save()
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    else:
        reg_form = RegForm()
    context = {
        'reg_form': reg_form
    }
    return render(request, 'register.html', context)
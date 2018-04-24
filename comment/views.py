from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Comment
from django.contrib.contenttypes.models import ContentType


def update_comment(request):
    user = request.user
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    print(referer)
    if not user.is_authenticated:
        return render(request, 'error.html', {'message': '用户未登录', 'redirect_to': referer})

    text = request.POST.get('text', '').strip()
    if text == '':
        return render(request, 'error.html', {'message': '评论内容为空', 'redirect_to': referer})

    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id'))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_object = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message': '评论对象不存在', 'redirect_to': referer})

    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_object
    comment.save()
    return redirect(referer)


import markdown
from django import  template
from django.contrib.auth.models import ContentType
from pyquery import PyQuery as pq

from comment.models import Comment
from comment.forms import CommentForm


register = template.Library()


@register.simple_tag()
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


@register.simple_tag()
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={'content_type': content_type.model, 'object_id': obj.pk, 'reply_comment_id': 0})
    return form


@register.simple_tag()
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')


@register.simple_tag()
def get_img_thumb(content, request):
    mark_content = markdown.markdown(content)
    html = pq(mark_content)
    # print(html.html())
    img = html('img').attr('src')
    if img:
        return img

    else:
        return 'http://{0}/static/image/bigIMG.jpg'.format(request.get_host())
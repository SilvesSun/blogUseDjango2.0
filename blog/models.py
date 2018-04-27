
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from ckeditor_uploader.fields import RichTextUploadingField

from read_statistics.models import ReadNumExpandMethod, ReadDetail
from mdeditor.fields import MDTextField


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50, verbose_name=u'标题')
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING, verbose_name=u'博客类型')
    content = MDTextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name=u'作者')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    read_details = GenericRelation(ReadDetail)

    class Meta:
        verbose_name = u"博客"
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title




from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
from django.utils import timezone
import os


class Post(models.Model):
    title_post = models.CharField(max_length=255, verbose_name='Title')
    author_post = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Author')
    data_post = models.DateTimeField(default=timezone.now, verbose_name='Data')
    content_post = models.TextField(verbose_name='Content')
    excerpt_post = models.TextField(verbose_name='Excerpt')
    category_post = models.ForeignKey(Category, on_delete=models.DO_NOTHING,
                                       blank=True, null=True, verbose_name='Category')
    image_post = models.ImageField(upload_to='post_img/%Y/%m/%d', blank=True,
                                    null=True, verbose_name='Image')
    published_post = models.BooleanField(default=False, verbose_name='Published')

    def __str__(self):
        return self.title_post
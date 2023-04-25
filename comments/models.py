from django.db import models
from posts.models import Post
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.conf import settings
import os


class Comment(models.Model):
    name_comment = models.CharField(max_length=150, verbose_name='Name')
    email_comment = models.EmailField(verbose_name='E-mail')
    comment = models.TextField(verbose_name='Comment')
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    date_comment = models.DateTimeField(default=timezone.now)
    published_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.name_comment

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image_post:
            self.resize_image(self.image_post.name, 800)

    @staticmethod
    def resize_image(img_name, new_width):
        img_path = os.path.join(settings.MEDIA_ROOT, img_name)
        img = Image.open(img_path)
        width, height = img.size
        new_height = round((new_width * height) / width)

        if width <= new_width:
            img.close()
            return

        new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        new_img.save(img_path,optimize=True,quality=60)
        new_img.close()




from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from django.urls import reverse
User=settings.AUTH_USER_MODEL

# Create your models here.
class TindaDates(models.Model):
    username=models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth=models.DateTimeField(auto_now_add=False)
    date_joined=models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=120, blank=True, null=True)
    image=models.ImageField(upload_to='media')

    def __str__(self):
        return self.username.username


class Category(models.Model):
    name=models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name

class UploadModel(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=120, blank=True, null=True)
    caption=models.CharField(max_length=120, blank=True, null=True)
    image=models.ImageField(upload_to='media')
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    likes=models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='like_post')
    
    def __str__(self):
        return self.name

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post=models.ForeignKey(UploadModel, on_delete=models.CASCADE, blank=True, null=True)
    text=models.CharField(max_length=500, blank=True, null=True)
    time_ns=models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('comment', kwargs={'pk':self.pk})




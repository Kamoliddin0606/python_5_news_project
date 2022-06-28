from email.mime import image
from email.policy import default
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from accounts.models import CustomUser
from taggit.managers import TaggableManager

from hitcount.utils import get_hitcount_model
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    image = models.ImageField(upload_to='Category')

    def __str__(self) -> str:
        return self.title
class Post(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='post')
    image = models.ImageField(upload_to='post_image')
    title = models.CharField(max_length=100)
    anons = models.CharField(max_length=250)
    discreption = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    tags = TaggableManager()
    

    def __str__(self) -> str:
        return self.title
    def get_count_of_likes(self):
        count = Like.objects.filter(post=self.id).count()
        print(count)
        return count
    def get_count_of_comments(self):
        count = self.PostComment.all().count()
        print(count)
        return count
    def get_count_of_views(self):
        count = get_hitcount_model().objects.get_for_object(self).hits
        print(count)
        return count
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE ,related_name='like')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1) 
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    like = models.BooleanField(default=False)

    def __str__(self) -> str:
        return  f'{self.author} - {self.like}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='PostComment')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='ParentComment', null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('created',)
    def __str__(self) -> str:
        return f'{self.author}--{self.body[:50]}...'

    def get_children(self):
        
        comments = Comment.objects.filter(parent_comment=self.id)
        count =comments.count()
        
        return comments
        
from email.policy import default
from enum import unique
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from hitcount.utils import get_hitcount_model
from uuid import uuid4
# Create your models here.
from PIL import Image
class CustomUser(AbstractUser):
    slug = models.SlugField(max_length=255, unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(upload_to='profile/', null=True, default='profile/default.png')
    phonenumber = PhoneNumberField(blank=True, null=True)
    def save(self,*args, **kwargs):
        print('check save')
        if not self.slug:
            slug = slugify(f'{self.username}-{uuid4()}')
            print(slug)
            self.slug =  slug
        super(CustomUser, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return f'{self.username}...'

    
    def count_procent(self):
     views = self.get_count_of_views()
     comments = self.get_count_of_comments()
     likes =  self.get_count_of_likes()
     maxcount = max(views,likes,comments)
     if maxcount ==0:
        maxcount=1
     viewsProcent = int((views/maxcount)*100) 
     likesProcent = int((likes/maxcount)*100) 
     commentsProcent = int((comments/maxcount)*100) 
     return {'Likes':{'procent':likesProcent,'count':likes},'Views':{'procent':viewsProcent,'count':views},'Comments':{'procent':commentsProcent,'count':comments}}
    def get_count_of_views(self):
        objects = self.post_set.all()
        count = 0
        for post in objects:
            count+=get_hitcount_model().objects.get_for_object(post).hits 
        return count        
        # objects = self.post_set.all()
        # count = 0
        # for post in objects:
        #     count+=get_hitcount_model().objects.get_for_object(post).hits

        # return count
        
    def get_count_of_comments(self):
        
        objects = self.post_set.all()
        count = 0
        for post in objects:
            count+=post.get_count_of_comments()

        return count
    def get_count_of_likes(self):
        
        objects = self.post_set.all()
        count = 0
        for post in objects:
            count+=post.get_count_of_likes()

        return count
    # def save(self, *args, **kwargs):
    #     super().save()

    #     img = Image.open(self.avatar.path)

    #     if img.height > 100 or img.width > 100:
    #         new_img = (100, 100)
    #         img.thumbnail(new_img)
    #         img.save(self.avatar.path)
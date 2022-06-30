from enum import unique
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
# Create your models here.
class CustomUser(AbstractUser):
    slug = models.SlugField(max_length=255, unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(upload_to='profile/', null=True)
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

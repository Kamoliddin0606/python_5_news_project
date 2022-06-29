import imp
from django.contrib import admin
from .models import *
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(BackGroundHeader)
# Register your models here.

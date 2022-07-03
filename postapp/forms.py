from dataclasses import fields
from unicodedata import category
from django import forms
from .models import Contact, Post
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','anons','image','discreption', 'category')

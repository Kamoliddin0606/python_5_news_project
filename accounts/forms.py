from dataclasses import fields
from xml.parsers.expat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UserCreationForm
from .models import CustomUser
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model =CustomUser
        fields =('username', 'email')

class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

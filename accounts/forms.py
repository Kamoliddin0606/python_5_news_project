from dataclasses import fields
from xml.parsers.expat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UserCreationForm
from .models import CustomUser
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email','avatar', 'bio', 'phonenumber')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model =CustomUser
        fields =('username', 'email','avatar', 'bio', 'phonenumber', 'first_name', 'last_name')

class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email','avatar', 'bio', 'phonenumber')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63,widget=forms.PasswordInput)
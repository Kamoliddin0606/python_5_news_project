from django.urls import path
from .views import loginview, logoutview, CreateUser,profile, editpost, detailpost
urlpatterns = [
    path('login/',loginview, name='login'),
    path('logout/',logoutview, name='logout'),
    path('registration/',CreateUser, name='registration'),
    path('profile/<slug:slug>',profile, name='profile'),
    path('profile/<slug:slug>/editpost/<int:id>',editpost, name='editpost'),
    path('profile/<slug:slug>/detailpost/<int:id>',detailpost, name='detailpost'),

]

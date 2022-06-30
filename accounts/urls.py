from django.urls import path
from .views import loginview, logoutview, CreateUser,profile
urlpatterns = [
    path('login/',loginview, name='login'),
    path('logout/',logoutview, name='logout'),
    path('registration/',CreateUser, name='registration'),
    path('profile/<slug:slug>',profile, name='profile'),

]

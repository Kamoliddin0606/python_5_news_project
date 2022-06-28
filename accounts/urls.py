from django.urls import path
from .views import loginview, logoutview, CreateUser
urlpatterns = [
    path('login/',loginview, name='login'),
    path('logout/',logoutview, name='logout'),
    path('registration/',CreateUser, name='registration')
]

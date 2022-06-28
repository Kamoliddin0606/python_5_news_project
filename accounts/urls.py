from django.urls import path
from .views import loginview, LogOut, CreateUser
urlpatterns = [
    path('login/',loginview, name='login'),
    path('logout/',LogOut.as_view(), name='logout'),
    path('registration/',CreateUser, name='registration')
]

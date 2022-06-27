from django.urls import path
from .views import Login, LogOut, CreateUser
urlpatterns = [
    path('login/',Login.as_view(), name='login'),
    path('logout/',LogOut.as_view(), name='logout'),
    path('registration/',CreateUser, name='registration')
]

from django.urls import path
from .views import loginview, logoutview, CreateUser,profile, editpost, detailpost, removepost, editprofile, detailpostprofile
urlpatterns = [
    path('login/',loginview, name='login'),
    path('logout/',logoutview, name='logout'),
    path('registration/',CreateUser, name='registration'),
    path('profile/<slug:slug>',profile, name='profile'),
    path('profile/<slug:slug>/<int:cat_id>',profile, name='profile'),
    path('profile/<slug:slug>/editpost/<int:id>',editpost, name='editpost'),
    path('profile/<slug:slug>/removepost/<int:id>',removepost, name='removepost'),
    path('profile/<slug:slug>/detailpost/<int:id>',detailpost, name='detailpost'),
    path('profile/<slug:slug>/addnewpost/',editpost, name='addnewpost'),
    path('profile/<slug:slug>/editprofile/',editprofile, name='editprofile'),
    path('profile/<slug:slug>/postdetail/<int:id>',detailpostprofile, name='detailpostprofile'),
]

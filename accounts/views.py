import os
from django.core.files.temp import NamedTemporaryFile
from traceback import print_tb
from unicodedata import category
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserCreateForm, LoginForm,UserChangeForm
from postapp.forms import PostForm
from .models import CustomUser
from django.contrib.auth import login, logout, authenticate
from postapp.models import Category
from postapp.models import Post, Like
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
import json
import datetime
from django.core.files import File  # you need this somewhere
import urllib
# class Login(LoginView):
#     template_name = 'registrations/login.html'

def loginview(request):
    
    if request.method == 'POST':
        postrequest = request.POST
        form =LoginForm(data=postrequest)
        print(form)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print(form.cleaned_data['username'],form.cleaned_data['password'])
            if user is not None:
                login(request=request, user=user)
                  
                message = f'Dear {user.username}! You have been logged in'
                request.session['message']= message
                return redirect('home')
            else:
                message = 'Login failed!'
                request.session['message']= message
                return redirect('login')
            


    return render(request=request, template_name='registrations/login.html', )
def logoutview(request):
    
    message = f'Dear {request.user.first_name}! You have been logged in'
    request.session['message']= message
    logout(request=request)
    return redirect('home')

def CreateUser(request):
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'): 
            user_form = UserCreateForm(data = request.POST)
            print(user_form)
            if user_form.is_valid():
                user = user_form.save() 
                user.set_password(request.POST.get('password1'))
                try:
                    user.save() 
                except:
                    print('err')
                message = 'The registration was successful. You can log in'
                request.session['message']= message
        # if form.is_valid():
            # form.save()
            return redirect('home')
        else:
            return redirect('registration')
    else:
        form = UserCreateForm()
    return render(request=request, template_name='registrations/registration.html', context={'form':form})
    
def profile(request, slug, cat_id=None):
    catsecond = None
    if Category.objects.all().count() <7 :
        catfirst = Category.objects.all()
    else:
        catfirst = Category.objects.all()[:6]
        catsecond = Category.objects.all()[6:]
    categories ={ 
        'catfirst':catfirst,
        'catsecond':catsecond,
        
    }
    if cat_id == None:
        
        posts = CustomUser.objects.get(slug=slug).post_set.all()
    else:
        print(type(cat_id))
        category = Category.objects.get(id=cat_id)
        posts = CustomUser.objects.get(slug=slug).post_set.filter(category=category)
    is_ajax =request.headers.get('X-Requested-With')== 'XMLHttpRequest'
    print(is_ajax)
    if request.method == 'GET' and  is_ajax:
        print(request.GET.get('test'))
        category = Category.objects.get(id=request.GET.get('cat_id'))
        posts = Post.objects.filter(category=category)
        data = serializers.serialize('json', posts)
        print(posts)
        
        return HttpResponse(data,
                         content_type="application/json")
    print(posts)
    context ={'posts':posts, 'categories':categories,'userprofile':CustomUser.objects.get(slug=slug)}
    return render(request=request, template_name='profile/profile.html', context=context)

def editpost(request, slug, id=None):
    
    categories = Category.objects.all()
    author = CustomUser.objects.get(slug=slug)
    # print(request.user.username,CustomUser.objects.get(slug=slug).username )
    post=None
    
    if request.user.slug == author.slug and id!=None:
        post = author.post_set.get(id=id)
    
    # print('_____test____')
    if request.method == 'POST':
        if post:
            form = PostForm(request.POST, request.FILES, instance=post)
            
            if form.is_valid():
                
                form.save()
                return redirect('profile', author.slug)
        else:
            form = PostForm(request.POST,request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = author
                post.save()
                return redirect('profile', author.slug)
        title  = request.POST.get('title')
        anons  = request.POST.get('anons')
        discreption  = request.POST.get('discreption')
        category  = request.POST.get('categories')
        image = request.FILES
        print(image)

        is_ajax = request.headers.get('X-Requested-With')== 'XMLHttpRequest'
        # print(request.FILES, '______POST')
        if is_ajax:
            print(request.POST)
            title = request.POST.get("title")
            discreption = request.POST.get("discreption")
            anons = request.POST.get('anons')
            category = request.POST.get('categories')
            print(title,anons,discreption,category)
                
            print('ajax')
            return JsonResponse({'result':True,})
    

                # print(request.GET.get('test'))
    context = {'categories':categories,'post':post,'userprofile':CustomUser.objects.get(slug=slug)}
    return render(request=request, template_name='profile/editpost.html', context=context)

def removepost(request, slug, id):
    post = Post.objects.filter(author=CustomUser.objects.get(slug=slug), id=id)
    if post:
        print(post)
        post.delete()
    else:
        print("I don't get your message")

    return redirect('profile', slug=slug)
def detailpost(request,slug, id):
    pass
def editprofile(request, slug):
    catsecond = None
    form = UserChangeForm()
    object = CustomUser.objects.get(slug=slug)
    categoriessellect = Category.objects.all()

    if Category.objects.all().count() <7 :
        catfirst = Category.objects.all()
    else:
        catfirst = Category.objects.all()[:6]
        catsecond = Category.objects.all()[6:]
    categories ={ 
        'catfirst':catfirst,
        'catsecond':catsecond,
        
    }
    if request.method == 'POST':
        print(request.POST.get('date_joined'))
        _mutable =request.POST._mutable
        request.POST._mutable = True
        request.POST['date_joined']=datetime.datetime.now()


        
        request.POST._mutable = _mutable
        form = UserChangeForm(request.POST, request.FILES, instance=object)
        
        print(form)
        if form.is_valid():
            print('_____ valid _____')
            profileuser = CustomUser.objects.filter(slug=slug)
            profileuser.update(
                username = request.POST.get('username'),
                email = request.POST.get('email'),
                bio = request.POST.get('bio'),
                avatar = request.POST.get('avatar'),
                phonenumber = request.POST.get('phonenumber'),
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
            )
            # if 'image' in request.FILES:
                
            #     profileuser.update(avatar=request.FILES['image'])  
               
          

            return redirect('profile', slug)
    

        is_ajax = request.headers.get('X-Requested-With')== 'XMLHttpRequest'
        # print(request.FILES, '______POST')
        if is_ajax:
            print(request.POST)
            title = request.POST.get("title")
            discreption = request.POST.get("discreption")
            anons = request.POST.get('anons')
            category = request.POST.get('categories')
            print(title,anons,discreption,category)
                
            print('ajax')
            return JsonResponse({'result':True,})
    

                # print(request.GET.get('test'))
    context = {'categories':categories,'categoriessellect':categoriessellect,'object':object, 'userprofile':object, 'form':form}
    return render(request=request, template_name='profile/editprofile.html', context=context)

def detailpostprofile(request, slug, id):
    author = CustomUser.objects.get(slug=slug)
    
    catsecond=None
    if id:
        post = Post.objects.get(id=id)
    if Category.objects.all().count() <7 :
        catfirst = Category.objects.all()
    else:
        catfirst = Category.objects.all()[:6]
        catsecond = Category.objects.all()[6:]
    categories ={ 
        'catfirst':catfirst,
        'catsecond':catsecond,
        
    }
    if request.method=='POST':
        likeObject = Like.objects.filter(post = post, author=author)
        if likeObject and likeObject[0].like==True:
            likeObject.update(like=False)
        elif likeObject and likeObject[0].like==False:
            likeObject.delete()
        else:
            Like.objects.create(author=author, post = post, like=True)
        return redirect('detailpostprofile', slug=slug, id=id)
    try:
        like = Like.objects.get(post= post, author=author)
    except:
        like=None


    context = {'categories':categories, 'userprofile':CustomUser.objects.get(slug=slug), 'post':post, 'like':like}
    return render(request=request, template_name='profile/detailpostprofile.html', context=context)
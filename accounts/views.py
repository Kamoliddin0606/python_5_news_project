from multiprocessing import managers
import os
from unicodedata import category
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserCreateForm, LoginForm
from postapp.forms import PostForm
from .models import CustomUser
from django.contrib.auth import login, logout, authenticate
from postapp.models import Category
from postapp.models import Post
from django.http import JsonResponse
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
                    print(err)
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
    
def profile(request, slug):
    if Category.objects.all().count() <7 :
        catfirst = Category.objects.all()
    else:
        catfirst = Category.objects.all()[:6]
        catsecond = Category.objects.all()[6:]
    categories ={ 
        'catfirst':catfirst,
        'catsecond':catsecond,
        
    }
   
    posts = CustomUser.objects.get(slug=slug).post_set.all()
    print(posts)
    context ={'posts':posts, 'categories':categories,'userprofile':CustomUser.objects.get(slug=slug)}
    return render(request=request, template_name='profile/profile.html', context=context)

def editpost(request, slug, id):
    
    categories = Category.objects.all()
    author = CustomUser.objects.get(slug=slug)
    # print(request.user.username,CustomUser.objects.get(slug=slug).username )
    post=''
    if request.user.slug == author.slug:
       post = author.post_set.get(id=id)
     
    # print('_____test____')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        
        if form.is_valid():
            
            form.save()
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

def detailpost(request,slug, id):
    pass
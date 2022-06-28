from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserCreateForm, LoginForm
from .models import CustomUser
from django.contrib.auth import login, logout, authenticate
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
                user.save() 
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
    
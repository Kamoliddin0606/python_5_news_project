from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserCreateForm
from .models import CustomUser
class Login(LoginView):
    template_name = 'registrations/login.html'
class LogOut(LogoutView):
    template_name= 'registrations/logout.html'

def CreateUser(request):
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'): 
            user_form = UserCreateForm(data = request.POST)
            print(user_form)
            if user_form.is_valid():
                user = user_form.save() 
                user.set_password(user.password)
                user.save() 
        # if form.is_valid():
            # form.save()
            return redirect('home')
        else:
            return redirect('registration')
    else:
        form = UserCreateForm()
    return render(request=request, template_name='registrations/registration.html', context={'form':form})
    
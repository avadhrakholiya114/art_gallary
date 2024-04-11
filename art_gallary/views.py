from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

# Create your views here.
# //artist 123
def home(request):
    return render(request, 'index.html')

def  about(request):
    return render(request, 'about.html')

def register(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2= request.POST.get('confirmPassword')
        email = request.POST.get('email')
        print(username, password, email)
        my_user=User.objects.create_user(username, email, password)
        my_user.save()
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


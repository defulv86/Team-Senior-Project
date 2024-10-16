from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from .backends import CustomUserBackend  # Import your custom backend
from .models import User  # Import your User model

def home(request):
    all_users = User.objects.all
    return render(request, 'home.html', {
        'all':all_users
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('passwd')

        # Use your custom backend to authenticate
        user = CustomUserBackend().authenticate(request, uname=username, passwd=password)

        if user is not None:
            auth_login(request, user)  # Log in the user
            return redirect('dashboard')  # Redirect to the dashboard
        else:
            return HttpResponse("Invalid username or password.")
    
    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)  # Logs out the user
    return redirect('login')  # Redirects to the login page after logout


def dashboard(request):
    if request.user.is_authenticated:
        # Your logic for rendering the dashboard goes here
        return render(request, 'dashboard.html')
    else:
        return redirect('login')  # Redirect to the login page if not authenticated

def testpage(request):
    return render(request, 'testpage.html')
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_backends
from django.contrib.auth.decorators import login_required
from .backends import CustomUserBackend  # Import your custom backend
from .models import User  # Import your User model

def home(request):
    all_users = User.objects.all
    return render(request, 'home.html', {
        'all':all_users
    })

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('passwd')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            # Redirect based on the user's staff status
            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('dashboard')
        else:
            error_message = "Invalid username or password."  # Set the error message
    
    return render(request, 'login.html', {'error_message': error_message})



def logout_view(request):
    auth_logout(request)  # Logs out the user
    return redirect('login')  # Redirects to the login page after logout


def dashboard(request):
    if request.user.is_authenticated:
        # Your logic for rendering the dashboard goes here
        return render(request, 'dashboard.html', {'user': request.user})
    else:
        return redirect('login')  # Redirect to the login page if not authenticated

def testpage(request):
    return render(request, 'testpage.html')
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import RegistrationForm

def home(request):
    all_users = User.objects.all()
    return render(request, 'home.html', {'all': all_users})

@login_required
def dashboard(request):
    if request.user.userprofile.permission_level == 1:
        return render(request, 'dashboard.html')
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

@login_required
def admin(request):
    if request.user.userprofile.permission_level == 2:
        return render(request, 'admin.html')
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

def promote_to_admin(user):
    user.userprofile.permission_level = 2
    user.userprofile.save()
    user.is_staff = True
    user.save()

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('passwd')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def testpage(request):
    return render(request, 'testpage.html')

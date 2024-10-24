from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm

def home(request):
    all_users = User.objects.all()
    return render(request, 'home.html', {'all': all_users})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

    else:
        return render(request, 'dashboard.html')

@login_required
def admin(request):
    if request.user.is_superuser:
        return render(request, 'admin.html')
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

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
        username = request.POST.get('username')
        password = request.POST.get('passwd')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def testpage(request):
    return render(request, 'testpage.html')

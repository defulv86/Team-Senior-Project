from django.shortcuts import render
from .models import User

def home(request):
    all_users = User.objects.all
    return render(request, 'home.html', {
        'all':all_users
    })

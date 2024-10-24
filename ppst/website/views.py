from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Ticket, Test, Result
from .forms import RegistrationForm
import json

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

@csrf_exempt
@login_required
def create_test(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        age = data.get('age')

        if age:
            # Create the test object
            test = Test.objects.create(user=request.user, age=age)
            
            # Build the full URL using the test link
            test_url = request.build_absolute_uri(f"/testpage/{test.link}")
            return JsonResponse({'test_link': test_url})
        else:
            return JsonResponse({'error': 'Invalid age'}, status=400)

def test_page_view(request, link):
    # Fetch the test associated with the given link
    test = get_object_or_404(Test, link=link)
    
    # Here you can render the test page with the test data
    return render(request, 'testpage.html', {'test': test})

@login_required
def get_test_results(request):
    tests = Test.objects.filter(user=request.user)
    test_data = [{
        'id': test.id,
        'status': 'complete' if test.finished_at else 'in_progress',
    } for test in tests]

    return JsonResponse({'tests': test_data})


@login_required
def test_results(request, test_id):
    try:
        test = Test.objects.get(id=test_id, user=request.user)
        if not test.finished_at:
            return JsonResponse({'error': 'Test is not completed'}, status=400)

        results = Result.objects.filter(test=test).values('fourdigit_accuracy_1', 'fourdigit_latency_1', 
                                                          'fivedigit_accuracy_1', 'fivedigit_latency_1')
        result_data = [{'metric': key, 'value': value} for result in results for key, value in result.items()]
        return JsonResponse({'results': result_data})

    except Test.DoesNotExist:
        return JsonResponse({'error': 'Test not found'}, status=404)


# Handle ticket submission (for non-staff users)
@login_required
def submit_ticket(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        description = request.POST.get('description')

        # Validate that category and description are not empty
        if not category or not description:
            return JsonResponse({'error': 'Please fill in all fields.'}, status=400)

        # Save ticket to the database
        Ticket.objects.create(user=request.user, category=category, description=description)
        return JsonResponse({'message': 'Ticket submitted successfully!'}, status=200)
    
    return JsonResponse({'error': 'Invalid request.'}, status=400)

# Fetch user's tickets
@login_required
def get_user_tickets(request):
    if request.method == 'GET':
        tickets = Ticket.objects.filter(user=request.user).values('category', 'description', 'created_at')
        return JsonResponse(list(tickets), safe=False)
    return JsonResponse({'error': 'Invalid request.'}, status=400)
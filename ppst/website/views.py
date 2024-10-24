from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Ticket, Test, Result
import json

def home(request):
    all_users = User.objects.all
    return render(request, 'home.html', {
        'all':all_users
    })

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
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

@login_required
def update_account(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        user = request.user

        # Check current password
        if not user.check_password(current_password):
            return JsonResponse({'error': 'Current password is incorrect.'}, status=400)

        # Update user details
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        
        # Update password if a new one is provided
        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # Keep user logged in after password change
        
        user.save()  # Save the updated user information
        return JsonResponse({'message': 'Account updated successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request.'}, status=400)
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from .models import Ticket, Test, Result, Aggregate, Stimulus, Response, Notification
from dateutil import parser
from statistics import mean
import json
def home(request):
    all_users = User.objects.all()  # Call the method to get all users
    return render(request, 'home.html', {
        'all': all_users
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

        if not age or int(age) < 18:
            return JsonResponse({'error': 'Invalid age: Age must be 18 or older to create a test.'}, status=400)

        if not age or int(age) > 99:
            return JsonResponse({'error': "Invalid age: Age must be between 18 and 99."}, status=400)

        # Explicitly set created_at to the current time
        test = Test.objects.create(
            user=request.user,
            age=age,
            created_at=timezone.now()  # Explicitly setting created_at
        )
        
        # Build the full URL using the test link
        test_url = request.build_absolute_uri(f"/testpage/{test.link}")
        return JsonResponse({'test_link': test_url})


def test_page_view(request, link):
    try:
        test = Test.objects.get(link=link)
        # Call different view functions based on test status
        if test.status == 'completed':
            return completionpage(request)
        elif test.status == 'invalid':
            return errorpage(request)
        elif test.status == 'pending':
            stimuli = Stimulus.objects.all()
            return render(request, 'testpage.html', {'test': test, 'stimuli': stimuli})
        else:
            return errorpage(request)  # For any other undefined statuses
    except Test.DoesNotExist:
        return render(request, '404.html')



@csrf_exempt
def submit_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            link = data['link']
            stimulus_id = data['stimulus_id']
            response_text = data['response_text']
            response_position = data['response_position']
            timestamps = data.get('timestamps', [])
            expected_stimulus = data['expected_stimulus']

            if not isinstance(timestamps, list):
                return JsonResponse({'error': 'Timestamps must be a list.'}, status=400)

            # Fetch the Test instance using the provided link
            test = Test.objects.get(link=link)
            stimulus = Stimulus.objects.get(id=stimulus_id)

            # Save the response instance
            response_instance = Response(
                response=response_text,
                test=test,
                stimulus=stimulus,
                response_position=response_position,
                time_submitted=timezone.now()
            )
            response_instance.save()

            # Calculate latencies for characters based on timestamps
            character_latencies = []
            if timestamps:
                reference_timestamp = timestamps[0]
                
                for index in range(1, len(timestamps)):
                    if index < len(response_text) + 1:
                        current_timestamp = timestamps[index]
                        latency = current_timestamp - reference_timestamp
                        character_latencies.append(round(latency, 2))
            
                        reference_timestamp = current_timestamp
            else:
                return JsonResponse({'error': 'No timestamps available.'}, status=400)

            # Determine expected number of latencies based on the expected stimulus
            if stimulus.stimulus_type.stimulus_type.startswith('4_Span'):
                expected_count = 4
            elif stimulus.stimulus_type.stimulus_type.startswith('5_Span'):
                expected_count = 5
            else:
                expected_count = len(expected_stimulus)

            # Truncate character_latencies to expected_count
            character_latencies = character_latencies[:expected_count]

            # Calculate accuracy for each character
            accuracy = []
            for i in range(min(len(response_text), len(expected_stimulus))):
                if response_text[i] == expected_stimulus[i]:
                    accuracy.append(1.0)  # Correct character
                else:
                    accuracy.append(0.0)  # Incorrect character

            if len(response_text) < len(expected_stimulus):
                accuracy.extend([0.0] * (len(expected_stimulus) - len(response_text)))

            # Increment amount correct based on the accuracy
            amount_correct = 0
            if len(response_text) == expected_count and all(a == 1.0 for a in accuracy):
                amount_correct += 1

            # Save latencies and accuracy in the Results table
            result, created = Result.objects.get_or_create(test=test)

            # Store latencies for this response position
            if response_position not in result.character_latencies:
                result.character_latencies[response_position] = []
            result.character_latencies[response_position].extend(character_latencies)

            # Store accuracies for this response position
            if response_position not in result.character_accuracies:
                result.character_accuracies[response_position] = []
            result.character_accuracies[response_position].extend(accuracy)

            result.amount_correct = (result.amount_correct or 0) + amount_correct

            result.save()  # Save the updated Result

            return JsonResponse({'status': 'success'})

        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except Test.DoesNotExist:
            return JsonResponse({'error': 'Test not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request.'}, status=400)

def check_test_status(request, link):
    if request.method == 'GET':  # Ensure the request is a GET request
        test = get_object_or_404(Test, link=link)  # Fetch the test by link
        test.check_status()  # Call any status update logic
        return JsonResponse({'status': test.status})
    else:
        # Return an error if the request method is not GET
        return JsonResponse({'error': 'Invalid request method. Only GET is allowed.'}, status=405)

def mark_test_complete(request, link):
    if request.method == 'POST':
        test = get_object_or_404(Test, link=link)
        test.finished_at = timezone.now()  # Set the finish time
        test.status = 'Completed'
        test.save()

        # Update or create the aggregate for the test's age group
        update_or_create_aggregate(test)

        # Create a notification for test completion
        Notification.objects.create(
            user=test.user,
            test=test,
            header="Test Completed",
            message=f"Your patient has completed the test for link: {test.link}. Results are available to view."
        )

        return JsonResponse({'status': 'success', 'message': 'Test marked as complete with finish time recorded.'})
    else:
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)
    
def invalidate_test(request, link):
    if request.method == 'POST':
        test = get_object_or_404(Test, link=link)
        test.premature_exit = True  # Mark as exited prematurely
        test.save()
        check_test_status(request, link)
        Notification.objects.create(
            user=test.user,
            test=test,
            header="Test Invalidated",
            message=f"Your patient has exited the test without completion for link: {test.link}. Do you want to create a test?"
        )
        
        return JsonResponse({"status": "canceled"})
    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)

def check_and_notify_test_status():
    """
    Periodically checks each test status to see if a warning or expiration notification should be sent.
    """
    now = timezone.now()
    tests = Test.objects.all()

    for test in tests:
        expiration_date = test.created_at + timedelta(weeks=1)
        time_until_expiry = expiration_date - now

        # Adjust the time checks to ensure precision with 24-hour notifications
        if timedelta(hours=23, minutes=59) < time_until_expiry <= timedelta(hours=24) and not test.finished_at:
            # Warning if time left is between 23 hours 59 minutes and exactly 24 hours
            if not Notification.objects.filter(test=test, header="Test Expiry Warning").exists():
                Notification.objects.create(
                    user=test.user,
                    test=test,
                    header="Test Expiry Warning",
                    message=f"Your patient has not started or completed the test yet. The test link ({test.link}) will expire in 24 hours if not completed.",
                )

        # Send expiration notification if the test is now expired
        elif time_until_expiry <= timedelta(0) and not test.finished_at:
            if not Notification.objects.filter(test=test, header="Test Expired").exists():
                Notification.objects.create(
                    user=test.user,
                    test=test,
                    header="Test Expired",
                    message=f"Test link {test.link} has expired because it was not completed in one week.",
                )
def start_test(request, link):
    if request.method == 'POST':
        test = get_object_or_404(Test, link=link)
        test.status = 'Pending'
        test.started_at = timezone.now()  # Set the start time
        test.save()

        Notification.objects.create(
            user=test.user,
            test=test,
            header="Test Started",
            message=f"The patient has officially started the test for link: {test.link}."
        )
        return JsonResponse({'status': 'success', 'message': 'Test start time recorded.'})
    else:
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)


@login_required
def get_test_results(request):
    tests = Test.objects.filter(user=request.user)
    
    # Update the status for each test based on conditions
    test_data = []
    for test in tests:
        test.check_status()  # Ensure the status is up-to-date
        test_data.append({
            'id': test.id,
            'link': test.link,
            'age': test.age,
            'created_at': test.created_at,
            'started_at': test.started_at,
            'finished_at': test.finished_at,
            'status': test.status,
        })

    return JsonResponse({'tests': test_data})

def get_stimuli(request):
    stimuli = Stimulus.objects.select_related('stimulus_type').all()
    
    # Organizing question presentation by type
    ordered_stimuli = {
        '4_Span_Digit_Pr': [],
        '5_Span_Digit_Pr': [],
        '4_Span_Digit': [],
        '5_Span_Digit': [],
        '4_Span_Mixed_Pr': [],
        '5_Span_Mixed_Pr': [],
        '4_Span_Mixed': [],
        '5_Span_Mixed': []
    }
    
    for stimulus in stimuli:
        if stimulus.stimulus_type.stimulus_type == '4_Span_Digit':
            ordered_stimuli['4_Span_Digit'].append(stimulus)
        elif stimulus.stimulus_type.stimulus_type == '5_Span_Digit':
            ordered_stimuli['5_Span_Digit'].append(stimulus)
        elif stimulus.stimulus_type.stimulus_type == '4_Span_Mixed':
            ordered_stimuli['4_Span_Mixed'].append(stimulus)
        elif stimulus.stimulus_type.stimulus_type == '5_Span_Mixed':
            ordered_stimuli['5_Span_Mixed'].append(stimulus)
        elif stimulus.stimulus_type.stimulus_type == '4_Span_Digit_Pr':
            ordered_stimuli['4_Span_Digit_Pr'].append(stimulus)
        elif stimulus.stimulus_type.stimulus_type == '5_Span_Digit_Pr':
            ordered_stimuli['5_Span_Digit_Pr'].append(stimulus)
        elif stimulus.stimulus_type.stimulus_type == '4_Span_Mixed_Pr':
            ordered_stimuli['4_Span_Mixed_Pr'].append(stimulus)
        elif stimulus.stimulus_type.stimulus_type == '5_Span_Mixed_Pr':
            ordered_stimuli['5_Span_Mixed_Pr'].append(stimulus)

    final_stimuli = (
        ordered_stimuli['4_Span_Digit_Pr'] +
        ordered_stimuli['5_Span_Digit_Pr'] +
        ordered_stimuli['4_Span_Digit'] +
        ordered_stimuli['5_Span_Digit'] +
        ordered_stimuli['4_Span_Mixed_Pr'] +
        ordered_stimuli['5_Span_Mixed_Pr'] +
        ordered_stimuli['4_Span_Mixed'] +
        ordered_stimuli['5_Span_Mixed']
    )

    # Convert to a list of dictionaries for JSON response
    response_data = [{'id': stim.id, 'stimulus_content': stim.stimulus_content, 'stimulus_type': stim.stimulus_type.stimulus_type} for stim in final_stimuli]
    
    return JsonResponse(response_data, safe=False)


@login_required
def test_results(request, test_id):
    # Retrieve test and result data
    test = get_object_or_404(Test, id=test_id)
    result = Result.objects.filter(test=test).first()
    
    if not result:
        return JsonResponse({"error": "No test results available for this test."}, status=404)

    # Retrieve age group aggregate data
    age_group = Aggregate.objects.filter(min_age__lte=test.age, max_age__gte=test.age).first()
    if not age_group:
        return JsonResponse({"error": "No aggregate data available for this age group."}, status=404)

    min_age = age_group.min_age
    max_age = age_group.max_age
    patient_age = test.age

    metrics = [
        'fourdigit_1', 'fourdigit_2', 'fourdigit_3',
        'fivedigit_1', 'fivedigit_2', 'fivedigit_3',
        'fourmixed_1', 'fourmixed_2', 'fourmixed_3',
        'fivemixed_1', 'fivemixed_2', 'fivemixed_3'
    ]

    excluded_positions = {"1", "2", "9", "10"}
    test_results = []
    aggregate_results = []
    metric_position = 3

    # Loop through each metric and calculate averages, excluding practice positions
    for metric in metrics:
        while str(metric_position) in excluded_positions:
            metric_position += 1

        # Retrieve user data for accuracies and latencies
        user_accuracies = result.character_accuracies.get(str(metric_position), [])
        user_latencies = result.character_latencies.get(str(metric_position), [])

        # Calculate accuracy and latency averages, using mean with 0 as fallback for empty lists
        user_accuracy_avg = round(sum(user_accuracies) / len(user_accuracies), 2) if user_accuracies else 0
        user_latency_avg = round(sum(user_latencies) / len(user_latencies), 2) if user_latencies else 0
        
        # Retrieve aggregate data for comparison
        avg_accuracy = age_group.average_accuracies.get(metric, 0)
        avg_latency = age_group.average_latencies.get(metric, 0)

        # Comparison logic for accuracy
        if user_accuracy_avg > avg_accuracy:
            accuracy_comparison = "Above average"
        elif user_accuracy_avg < avg_accuracy:
            accuracy_comparison = "Below average"
        else:
            accuracy_comparison = "Average"

        # Comparison logic for latency
        if user_latency_avg < avg_latency:  # Lower latency is better
            latency_comparison = "Below average"
        elif user_latency_avg > avg_latency:
            latency_comparison = "Above average"
        else:
            latency_comparison = "Average"

        # Append accuracy and latency results
        test_results.append({
            "metric": f"{metric} Accuracy",
            "values": user_accuracies,
            "average": user_accuracy_avg,
            "aggregate_average": avg_accuracy,
            "comparison": accuracy_comparison
        })
        test_results.append({
            "metric": f"{metric} Latency",
            "values": user_latencies,
            "average": user_latency_avg,
            "aggregate_average": avg_latency,
            "comparison": latency_comparison
        })

        aggregate_results.append({
            "metric": f"{metric} Accuracy",
            "average": avg_accuracy
        })
        aggregate_results.append({
            "metric": f"{metric} Latency",
            "average": avg_latency
        })

        metric_position += 1

    # Calculate amount correct for non-practice questions
    amount_correct = sum(
        1 for pos, accuracy in result.character_accuracies.items()
        if pos not in excluded_positions and all(a == 1 for a in accuracy)
    )

    return JsonResponse({
        "test_id": test_id,
        "test_results": test_results,
        "aggregate_results": aggregate_results,
        "amount_correct": amount_correct,
        "min_age": min_age,
        "max_age": max_age,
        "patient_age": patient_age
    })

def get_test_comparison_data(request, test_id):
    test = Test.objects.get(id=test_id)
    result = Result.objects.get(test=test)
    age = test.age

    # Find the matching aggregate based on age
    aggregate = Aggregate.objects.filter(min_age__lte=age, max_age__gte=age).first()

    if not aggregate:
        return JsonResponse({'error': 'No matching aggregate data found'}, status=404)

    # Define positions to exclude (practice questions)
    excluded_positions = {"1", "2", "9", "10"}
    
    # Calculate averages for patient data excluding practice questions
    patient_latencies = {
        pos: mean(values) for pos, values in result.character_latencies.items()
        if pos not in excluded_positions and values
    }
    patient_accuracies = {
        pos: mean(values) for pos, values in result.character_accuracies.items()
        if pos not in excluded_positions and values
    }
    
    # Calculate averages for aggregate data in the same way
    aggregate_latencies = {
        pos: avg for pos, avg in aggregate.average_latencies.items() if pos not in excluded_positions
    }
    aggregate_accuracies = {
        pos: avg for pos, avg in aggregate.average_accuracies.items() if pos not in excluded_positions
    }

    # Prepare data for chart
    data = {
        "patient": {
            "latencies": patient_latencies,
            "accuracies": patient_accuracies,
            "amount_correct": result.amount_correct,
        },
        "aggregate": {
            "latencies": aggregate_latencies,
            "accuracies": aggregate_accuracies,
        },
    }
    return JsonResponse(data)

def update_or_create_aggregate(test):
    """
    Updates or creates an aggregate entry for the age group associated with the completed test.
    """
    # Define the special age group for ages 18-29
    age = test.age
    if 18 <= age <= 29:
        min_age, max_age = 18, 29
    else:
        min_age = (age // 10) * 10
        max_age = min_age + 9

    # Check if an aggregate for this age group already exists
    age_group, created = Aggregate.objects.get_or_create(
        min_age=min_age,
        max_age=max_age,
        defaults={"average_latencies": {}, "average_accuracies": {}}
    )

    # Retrieve all relevant results within this age group
    results_in_age_group = Result.objects.filter(test__age__gte=min_age, test__age__lte=max_age)

    # Initialize dictionaries to store sums and counts for averages
    latencies_sums = {}
    accuracies_sums = {}
    counts = {}

    # Define the metrics and excluded positions
    metrics = [
        'fourdigit_1', 'fourdigit_2', 'fourdigit_3',
        'fivedigit_1', 'fivedigit_2', 'fivedigit_3',
        'fourmixed_1', 'fourmixed_2', 'fourmixed_3',
        'fivemixed_1', 'fivemixed_2', 'fivemixed_3'
    ]
    excluded_positions = {"1", "2", "9", "10"}
    
    # Start metric_position at 3 as specified
    metric_position = 3

    # Initialize sums and counts for each metric
    for metric in metrics:
        latencies_sums[metric] = 0
        accuracies_sums[metric] = 0
        counts[metric] = 0

    # Aggregate data from each result in the age group
    for result in results_in_age_group:
        metric_position = 3  # Reset to 3 for each result
        for metric in metrics:
            # Skip excluded positions
            while str(metric_position) in excluded_positions:
                metric_position += 1

            # Retrieve accuracy and latency lists for each metric by position
            accuracy_values = result.character_accuracies.get(str(metric_position), [])
            latency_values = result.character_latencies.get(str(metric_position), [])

            # Sum values and count entries to calculate averages only if lists are not empty
            if accuracy_values:
                accuracies_sums[metric] += sum(accuracy_values)
                counts[metric] += len(accuracy_values)
            if latency_values:
                latencies_sums[metric] += sum(latency_values)

            # Move to the next metric position
            metric_position += 1

    # Calculate the average for each metric and update the age group data
    average_accuracies = {}
    average_latencies = {}

    for metric in metrics:
        if counts[metric] > 0:
            average_accuracies[metric] = round(accuracies_sums[metric] / counts[metric], 2)
            average_latencies[metric] = round(latencies_sums[metric] / counts[metric], 2)
        else:
            average_accuracies[metric] = "N/A"
            average_latencies[metric] = "N/A"

    # Update or create the aggregate entry
    age_group.average_accuracies = average_accuracies
    age_group.average_latencies = average_latencies
    age_group.save()

    return age_group


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
        if new_password:  # Only update if new password is given
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # Keep user logged in after password change

        user.save()  # Save the updated user information
        return JsonResponse({'message': 'Account updated successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request.'}, status=400)

# Additional view to get user information for pre-filling the form
@login_required
def get_user_info(request):
    if request.method == 'GET':
        user = request.user
        user_info = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        return JsonResponse(user_info)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def get_user_notifications(request, load_type):
    
    if request.method == 'GET':
        if load_type != 'read' and load_type != 'unread':
            return JsonResponse({'error': 'Invalid request'}, status=400)
        
        tests = Test.objects.filter(user=request.user)
        if load_type == 'read':
            notifications = Notification.objects.filter(test__in=tests, is_archived=False, is_read=True).values('id','header', 'message', 'time_created', 'is_archived','is_read').order_by('-time_created')
        elif load_type == 'unread':
            notifications = Notification.objects.filter(test__in=tests, is_archived=False, is_read=False).values('id','header', 'message', 'time_created', 'is_archived').order_by('-time_created')
        data = {
            "notifications": list(notifications),
        }
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def dismiss_notification(request, id):
    if request.method == 'PATCH':
        try:
            notif = Notification.objects.get(id=id)
            notif.is_archived = True
            notif.is_read = True
            notif.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'not found'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def mark_as_read(request, id):
    if request.method == 'PATCH':
        try:
            notif = Notification.objects.get(id=id)
            notif.is_read = True
            notif.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'not found'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def errorpage(request):
    return render(request, 'errorpage.html')

def completionpage(request):
    return render(request, 'completionpage.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Ticket, Test, Result, Aggregate, Stimulus, Response, Notification, Registration
from dateutil import parser
from statistics import mean
import json

def home(request):
    """
    Displays the home page, which lists all registered users.

    :param request: The request object
    :return: The rendered home page
    """
    all_users = User.objects.all()  # Call the method to get all users
    return render(request, 'home.html', {
        'all': all_users
    })

def login_view(request):
    """
    Handles the login view by authenticating the user and redirecting them to the appropriate dashboard.

    :param request: The request object
    :return: The rendered login page with an error message if the credentials are invalid
    """
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
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            error_message = "Invalid username or password."  # Set the error message

    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('dashboard')

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    return render(request, 'login.html', {'error_message': error_message})

def register_view(request):
    """
    Handles the registration view by allowing users to request an account and sends a notification to all staff members.

    :param request: The request object
    :return: The rendered registration page with an error message if the registration request was invalid
    """
    error_message = None
    success_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('passwd')
        confirm_password = request.POST.get('confirm-passwd')

        if password != confirm_password:
            error_message = "Passwords do not match."
        else:
            # Check if the username already exists
            if Registration.objects.filter(username=username).exists():
                error_message = "Username already taken. Please choose a different username."
            else:
                # Save the registration request with plain text password (temporarily) and send a notification to all staff members
                try:
                    admins = User.objects.filter(is_staff=True)
                    for user in admins:
                        Notification.objects.create(
                            user=user,
                            info = f"registration:{username}",
                            header="New registration request",
                            message=f"The user {username}, has requested the creation of a new account. Please proceed to the registration tab to approve or deny."
                        )


                    registration = Registration(username=username, password=password)
                    registration.save()
                    success_message = "Your registration request has been submitted for admin approval."
                    return redirect('home')
                except Exception as e:
                    error_message = f"An error occurred: {e}"

    return render(request, 'register.html', {
        'error_message': error_message,
        'success_message': success_message
    })


def logout_view(request):
    """
    Logs out the user and redirects to the login page.

    :param request: The request object
    :return: Redirect to the login page
    """
    auth_logout(request)  # Logs out the user
    return redirect('login')  # Redirects to the login page after logout


def dashboard(request):
    """
    Renders the dashboard page. If the user is not authenticated, redirects to the login page.

    :param request: The request object
    :return: The rendered dashboard page
    """
    if request.user.is_authenticated and not request.user.is_staff:
        # Your logic for rendering the dashboard goes here
        return render(request, 'dashboard.html', {'user': request.user})
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('login')  # Redirect to the login page if not authenticated

def admin_dashboard(request):
    """
    Renders the administrator dashboard page. If the user is not authenticated, redirects to the login page.

    :param request: The request object
    :return: The rendered administrator dashboard page
    """
    if request.user.is_authenticated and request.user.is_staff:
        # Your logic for rendering the dashboard goes here
        return render(request, 'admin_dashboard.html', {'user': request.user})
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('dashboard')
    else:
        return redirect('login')  # Redirect to the login page if not authenticated

def get_registration_requests(request):
    """
    Returns a JSON response containing a list of unapproved registration requests.

    :param request: The request object
    :return: A JsonResponse containing a list of unapproved registration requests
    """

    if request.user.is_staff:
        registrations = Registration.objects.filter(approved=False)
        registration_data = [
            {
                "id": registration.id,
                "username": registration.username,
            }
            for registration in registrations
        ]
        return JsonResponse(registration_data, safe=False)
    else:
        return JsonResponse({"error": "Unauthorized"}, status=403)

#archive all unarchived notifications associated with a registration request
def remove_reg_notifs(registration):
    """
    Deletes all unarchived notifications associated with a registration request.

    :param registration: The registration object for which notifications should be removed.
    """
    registration_notifications = Notification.objects.filter(info=f"registration:{registration.username}", is_archived=False)
    for notification in registration_notifications:
        notification.delete()

@csrf_exempt
def approve_registration(request, registration_id):
    """
    Approves a registration request and creates a new user account with a hashed password.
    
    :param request: The request object
    :param registration_id: The ID of the registration request to approve
    :return: A JsonResponse indicating the success of the operation
    """
    
    if request.user.is_staff and request.method == 'POST':
        try:

            registration = Registration.objects.get(id=registration_id)

            remove_reg_notifs(registration)

            # Create a new user with a hashed password
            user = User.objects.create(
                username=registration.username,
                password=make_password(registration.password)  # Hash password here
            )
            registration.approved = True
            registration.save()
            return JsonResponse({"success": True})
        except Registration.DoesNotExist:
            return JsonResponse({"error": "Registration not found"}, status=404)
    return JsonResponse({"error": "Unauthorized"}, status=403)
@csrf_exempt
def deny_registration(request, registration_id):
    """
    Deletes a registration request and its associated notifications.

    :param request: The request object
    :param registration_id: The ID of the registration request to deny
    :return: A JsonResponse indicating the success of the operation
    """
    if request.user.is_staff and request.method == 'POST':
        try:
            registration = Registration.objects.get(id=registration_id)
            remove_reg_notifs(registration)
            registration.delete()
            return JsonResponse({"success": True})
        except Registration.DoesNotExist:
            return JsonResponse({"error": "Registration not found"}, status=404)
    return JsonResponse({"error": "Unauthorized"}, status=403)

@csrf_exempt
@login_required
def create_test(request):
    """
    Creates a new test for the logged-in user with the provided age.
    
    :param request: The request object
    :return: A JsonResponse containing the test link
    """
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

@login_required
def delete_invalid_test(request, test_id):
    """
    Deletes a specific invalid test if it belongs to the logged-in user and is marked as invalid.

    Args:
        request: The HTTP request object.
        test_id: The ID of the test to be deleted.

    Returns:
        JsonResponse: A JSON response indicating success or failure.
    """
    test = get_object_or_404(Test, id=test_id, user=request.user)

    if test.status != 'invalid':
        return HttpResponseForbidden("You can only delete tests marked as 'invalid'.")

    test.delete()
    return JsonResponse({"message": "Test deleted successfully.", "test_id": test_id})

def test_page_view(request, link):
    """
    Handles test page requests and renders the appropriate template based on the test status
    (completed, invalid, or pending). If the test is not found, a 404 page is rendered.

    :param request: The request object
    :param link: The link of the test to be rendered
    :return: A rendered HttpResponse object
    """
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
        
    """
    Handles the submission of a response for a specific test and stimulus. It processes the
    response data, calculates character latencies and accuracies, and updates the corresponding
    test results.

    :param request: The HTTP request object containing the response data.
    :return: A JsonResponse indicating the success of the operation or an error message if
             any issues occurred during processing.
    
    The request must be a POST request with a JSON body containing the following fields:
        - link: The link of the test.
        - stimulus_id: The ID of the stimulus.
        - response_text: The text response submitted by the user.
        - response_position: The position of the response.
        - timestamps: A list of timestamps for character inputs.
        - expected_stimulus: The expected stimulus for accuracy comparison.

    Errors:
        - Returns a 400 error if timestamps are not a list or if a field is missing.
        - Returns a 404 error if the test is not found.
        - Returns a 500 error for any other exceptions.
        - Returns a 400 error if the request is not a POST request.
    """
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
    """
    Retrieve the status of a test by its link.

    Args:
        request: The Django request object.
        link: The link to the test.

    Returns:
        A JSON response containing the status of the test.

    Raises:
        405: Method Not Allowed if the request method is not GET.
    """
    if request.method == 'GET':  # Ensure the request is a GET request
        test = get_object_or_404(Test, link=link)  # Fetch the test by link
        test.check_status()  # Call any status update logic
        return JsonResponse({'status': test.status})
    else:
        # Return an error if the request method is not GET
        return JsonResponse({'error': 'Invalid request method. Only GET is allowed.'}, status=405)

def mark_test_complete(request, link):
    """
    Mark a test as completed and set the finish time.

    Args:
        request: The Django request object.
        link: The link to the test.

    Returns:
        A JSON response indicating success or failure.

    Raises:
        405: Method Not Allowed if the request method is not POST.
    """
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
            header="Test Completed",
            message=f"Your patient has completed the test for link: {test.link}. Results are available to view."
        )

        return JsonResponse({'status': 'success', 'message': 'Test marked as complete with finish time recorded.'})
    else:
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)
    
def invalidate_test(request, link):
    """
    Invalidate a test by marking it as exited prematurely and notify the user that a patient exited the test without completion.

    Args:
        request: The Django request object.
        link: The link to the test.

    Returns:
        A JSON response indicating success or failure.

    Raises:
        405: Method Not Allowed if the request method is not POST.
    """
    if request.method == 'POST':
        test = get_object_or_404(Test, link=link)
        test.premature_exit = True  # Mark as exited prematurely
        test.save()
        check_test_status(request, link)
        Notification.objects.create(
            user=test.user,
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
                    header="Test Expiry Warning",
                    message=f"Your patient has not started or completed the test yet. The test link ({test.link}) will expire in 24 hours if not completed.",
                )

        # Send expiration notification if the test is now expired
        elif time_until_expiry <= timedelta(0) and not test.finished_at:
            if not Notification.objects.filter(test=test, header="Test Expired").exists():
                Notification.objects.create(
                    user=test.user,
                    header="Test Expired",
                    message=f"Test link {test.link} has expired because it was not completed in one week.",
                )

def start_test(request, link):
    """
    Record the start time of the test and update the test status to 'Pending' once the patient has officially started the test.

    Args:
        request: The Django request object.
        link: The link to the test.

    Returns:
        A JSON response indicating success or failure.

    Raises:
        405: Method Not Allowed if the request method is not POST.
    """
    if request.method == 'POST':
        test = get_object_or_404(Test, link=link)
        test.status = 'Pending'
        test.started_at = timezone.now()  # Set the start time
        test.save()

        Notification.objects.create(
            user=test.user,
            header="Test Started",
            message=f"The patient has officially started the test for link: {test.link}."
        )
        return JsonResponse({'status': 'success', 'message': 'Test start time recorded.'})
    else:
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)


@login_required
def get_test_results(request, test_status):
    """
    Retrieve a list of tests for the current user, filtered by test status.

    Args:
        request: The Django request object.
        test_status: The status of the test to filter by. Options are 'All', 'Pending', 'Completed', 'Invalid'.
    
    Returns:
        A JSON response containing a list of dictionaries representing the tests. Each dictionary contains the following keys:
            id: The ID of the test.
            link: The link to the test.
            age: The age of the patient taking the test.
            created_at: The date and time the test was created.
            started_at: The date and time the test was started.
            finished_at: The date and time the test was finished.
            status: The current status of the test.
    """
    tests = []
    if test_status == "All":
        tests = Test.objects.filter(user=request.user)
    elif test_status == "Pending":
        tests = Test.objects.filter(user=request.user, status='pending')
    elif test_status == "Completed":
        tests = Test.objects.filter(user=request.user, status='completed')
    elif test_status == "Invalid":
        tests = Test.objects.filter(user=request.user, status='invalid')

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
    """
    Retrieves and organizes stimuli from the database, categorizing them based on their stimulus type.

    Args:
        request: The Django request object.

    Returns:
        JsonResponse: A JSON response containing a list of dictionaries, where each dictionary represents a stimulus
        with its id, content, and type. Stimuli are ordered by their type in the response.
    """
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



# Helper function to format timestamps with seconds case.
def format_timestamp(timestamp):
    """
    Format a timestamp as a string, either from a datetime object or an ISO-formatted string.
    
    If the timestamp is a string, it is first converted to a datetime object using
    datetime.fromisoformat(). If the conversion fails, the original string is returned.
    
    If the timestamp is a datetime object, it is first converted to the local timezone
    (EST) using timezone.localtime(). The formatted time is then generated as a string
    in the format "YYYY-MM-DD | HH:MM:SS AM/PM", where the seconds are only included if
    they are not zero.
    
    Args:
        timestamp (str or datetime): The timestamp to be formatted.
    
    Returns:
        str: The formatted timestamp string.
    """
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            return timestamp
    
    if isinstance(timestamp, datetime):
        timestamp = timezone.localtime(timestamp)  # Convert to local timezone (EST)
        formatted_time = timestamp.strftime("%Y-%m-%d | %I:%M")
        if timestamp.second > 0:
            formatted_time += f":{timestamp.second:02d}"
        formatted_time += f" {timestamp.strftime('%p')}"
        return formatted_time
    
    return timestamp

# Helper function to format durations
def format_duration(duration):
    """
    Format a duration as a string, showing hours, minutes, and seconds separately.
    
    If the duration is zero, the function returns "0 seconds". If the duration is less
    than one hour, only minutes and seconds are shown. If the duration is less than one
    minute, only seconds are shown.
    
    Args:
        duration (timedelta): The duration to be formatted.
    
    Returns:
        str: The formatted duration string.
    """
    hours = duration.total_seconds() // 3600
    minutes = (duration.total_seconds() % 3600) // 60
    seconds = duration.total_seconds() % 60

    formatted_time = ''

    if hours > 0:
        formatted_time += f"{int(hours)} hour{'s' if hours > 1 else ''}"

    if minutes > 0 or hours > 0:  # Show minutes if hours or prior units are non-zero
        if formatted_time:
            formatted_time += ' '
        formatted_time += f"{int(minutes)} minute{'s' if minutes > 1 else ''}"

    if seconds > 0 or (not hours and not minutes):  # Show seconds if no hours and minutes
        if formatted_time:
            formatted_time += ' '
        formatted_time += f"{int(seconds)} second{'s' if seconds > 1 else ''}"

    return formatted_time or "0 seconds"

@login_required
def test_results(request, test_id):
    # Retrieve test and result data
    """
    View to display the results of a completed test.

    Retrieves a test and its associated result, and age group aggregate data.
    Calculates the completion time, and formats the timestamps for completed,
    pending, and invalid tests.
    Retrieves stimuli and associated responses for the export.
    Retrieves completed tests and calculates completion times.
    Retrieves pending tests and formats the timestamps with expiration and time remaining.
    Retrieves invalid tests and formats the timestamps with time since invalidation.
    Calculates accuracy and latency averages for each metric, excluding practice positions.
    Compares these averages to the aggregate data for the age group.
    Calculates the amount correct for non-practice questions.
    Returns a JSON response containing the test and result data, age group aggregate data,
    and the formatted test results, including accuracy and latency averages, and the amount correct.

    Parameters:
    test_id (int): The ID of the test to retrieve the results for.

    Returns:
    JsonResponse: A JSON response containing the test and result data, age group aggregate data,
    and the formatted test results, including accuracy and latency averages, and the amount correct.
    """
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
    test_link = test.link

    # Retrieve stimuli and associated responses for the export
    responses = Response.objects.filter(test=test).select_related('stimulus')
    stimuli_responses = []
    practice_correct = 0
    actual_correct = 0

    for index, response in enumerate(responses, start=1):
        stimulus = response.stimulus

        # Sort alphanumerically for "Correct Answer for Stimuli"
        correct_answer = ''.join(sorted(stimulus.stimulus_content))
        is_correct = response.response == correct_answer
        # Check if the stimulus is practice or actual
        if "Pr" in stimulus.stimulus_type.stimulus_type:
            practice_correct += int(is_correct)
        else:
            actual_correct += int(is_correct)

        stimuli_responses.append({
            "stimulus_id": stimulus.id,
            "stimulus_content": stimulus.stimulus_content,
            "correct_answer": correct_answer,
            "stimulus_type": stimulus.stimulus_type.stimulus_type,
            "response": response.response,
            "is_correct": is_correct,
            "time_submitted": format_timestamp(response.time_submitted)
        })

    # Calculate total correct
    total_correct = practice_correct + actual_correct

    # Retrieve completed tests and calculate completion times
    completed_tests = Test.objects.filter(
        status="completed", user=request.user
    ).values(
        "id", "link", "age", "user__username", "created_at", "started_at", "finished_at"
    )

    # Format the timestamps and calculate completion time
    formatted_completed_tests = []
    for test in completed_tests:
        # Calculate completion time if both started_at and finished_at are present
        if test["started_at"] and test["finished_at"]:
            started_at = test["started_at"]
            finished_at = test["finished_at"]
            completion_time = finished_at - started_at
            completion_time_str = format_duration(completion_time)  # Format duration including seconds
        else:
            completion_time_str = ""  # Leave empty if either timestamp is missing

        formatted_completed_tests.append({
            "id": test["id"],
            "link": test["link"],
            "age": test["age"],
            "user__username": test["user__username"],
            "created_at": format_timestamp(test["created_at"]),
            "started_at": format_timestamp(test["started_at"]),
            "finished_at": format_timestamp(test["finished_at"]),
            "completion_time": completion_time_str,  # Add completion time here
        })


    # Retrieve pending tests
    pending_tests = Test.objects.filter(
        status="pending", user=request.user
    ).values(
        "id", "link", "age", "user__username", "created_at"
    )

    # Format the timestamps for pending tests, with expiration and time remaining
    formatted_pending_tests = []
    for test in pending_tests:
        created_at = test["created_at"]
        expiration_date = created_at + timedelta(weeks=1)
        time_remaining = expiration_date - timezone.now()

        if time_remaining.total_seconds() > 0:
            days = time_remaining.days
            hours, remainder = divmod(time_remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Format time_remaining with conditions for non-zero units
            formatted_time_remaining = []
            if days > 0:
                formatted_time_remaining.append(f"{days} days")
            if hours > 0 or days > 0:  # Show hours if any prior unit is non-zero
                formatted_time_remaining.append(f"{hours} hours")
            if minutes > 0 or hours > 0 or days > 0:  # Show minutes if any prior unit is non-zero
                formatted_time_remaining.append(f"{minutes} minutes")
            formatted_time_remaining.append(f"{seconds} seconds")

            formatted_time_remaining = ", ".join(formatted_time_remaining)
        else:
            formatted_time_remaining = "Expired"

        formatted_pending_tests.append({
            "id": test["id"],
            "link": test["link"],
            "age": test["age"],
            "user__username": test["user__username"],
            "created_at": format_timestamp(created_at),
            "expiration_date": format_timestamp(expiration_date),
            "time_remaining": formatted_time_remaining
        })

    # Retrieve invalid tests
    invalid_tests = Test.objects.filter(
        status="invalid", user=request.user
    ).values(
        "id", "link", "age", "user__username", "created_at", "premature_exit"
    )

    # Format invalid tests with time since invalidation
    formatted_invalid_tests = []
    for test in invalid_tests:
        created_at = test["created_at"]
        if test["premature_exit"]:
            invalidated_at = created_at  # Invalidated at creation due to premature exit
        else:
            invalidated_at = created_at + timedelta(weeks=1)  # Invalidated after expiration

        # Calculate time since invalidation
        time_since_invalid = timezone.now() - invalidated_at
        days, remainder = divmod(time_since_invalid.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        formatted_time_since_invalid = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
        formatted_invalid_tests.append({
            "id": test["id"],
            "link": test["link"],
            "age": test["age"],
            "user__username": test["user__username"],
            "created_at": format_timestamp(created_at),
            "invalidated_at": format_timestamp(invalidated_at),
            "time_since_invalid": formatted_time_since_invalid
        })

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
            "metric": f"{metric}",
            "user_accuracy_values": user_accuracies,
            "user_accuracy_average": user_accuracy_avg,
            "accuracy_average": avg_accuracy,
            "accuracy_comparison": accuracy_comparison,
            "user_latency_values": user_latencies,
            "user_latency_average": user_latency_avg,
            "latency_average": avg_latency,
            "latency_comparison": latency_comparison
        })
        aggregate_results.append({
            "metric": f"{metric}",
            "accuracy_average": avg_accuracy,
            "latency_average": avg_latency
        })
        metric_position += 1

    # Calculate amount correct for non-practice questions
    amount_correct = sum(
        1 for pos, accuracy in result.character_accuracies.items()
        if pos not in excluded_positions and all(a == 1 for a in accuracy)
    )

    return JsonResponse({
        "test_id": test_id,
        "test_link": test_link,
        "test_results": test_results,
        "aggregate_results": aggregate_results,
        "amount_correct": amount_correct,
        "min_age": min_age,
        "max_age": max_age,
        "patient_age": patient_age,
        # Below is only needed for spreadsheet exportation.
        "stimuli_responses": stimuli_responses,
        "practice_correct": practice_correct,
        "actual_correct": actual_correct,
        "total_correct": total_correct,
        "completed_tests": formatted_completed_tests,
        "pending_tests": formatted_pending_tests,
        "invalid_tests": formatted_invalid_tests
    })

def get_test_comparison_data(request, test_id):
    """
    Retrieve and compare test results for a given test ID against aggregate data.

    This function fetches the test and result objects associated with a given test ID.
    It then determines the age of the test subject and retrieves the corresponding 
    aggregate data for the age group. The function calculates average latencies and 
    accuracies for both the patient and the aggregate data, excluding specified practice 
    question positions. The function returns the data in JSON format, containing a 
    comparison of the patient's performance against the aggregate data.

    Args:
        request: The HTTP request object.
        test_id (int): The ID of the test for which to retrieve comparison data.

    Returns:
        JsonResponse: A JSON response containing patient's test data, aggregate data, 
                      and a potential error message if no matching aggregate data is found.
    """
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
        "age_group": {
        "min_age": aggregate.min_age,
        "max_age": aggregate.max_age,
        }
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
    """
    Handles ticket submission for non-staff users.

    If the request method is POST, validates that the category and description
    fields are not empty. If valid, saves the ticket to the database and creates
    a notification for all admin users. Returns a success JSON response with a
    message.

    If the request method is not POST, or if the category or description fields
    are empty, returns a JSON error response with a status code of 400.
    """
    if request.method == 'POST':
        category = request.POST.get('category')
        description = request.POST.get('description')

        # Validate that category and description are not empty
        if not category or not description:
            return JsonResponse({'error': 'Please fill in all fields.'}, status=400)

        # Save ticket to the database
        new_ticket = Ticket.objects.create(user=request.user, category=category, description=description)

        #create a notification to alert admins of the issue
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            Notification.objects.create(
                                user=admin,
                                header=f"New support ticket",
                                info = f"{new_ticket.id}",
                                message=f"The user {new_ticket.user.username} has created a new {new_ticket.category} support ticket. Please review in the Support tab."
                            )
        return JsonResponse({'message': 'Ticket submitted successfully!'}, status=200)
    
    return JsonResponse({'error': 'Invalid request.'}, status=400)

# Fetch user's tickets
@login_required
def get_user_tickets(request):
    """
    Fetches the logged-in user's tickets along with their statuses.
    """
    if request.method == 'GET':
        tickets = Ticket.objects.filter(user=request.user).select_related('user').values(
            'id', 'category', 'description', 'created_at', 'status', 'user__username'
        )
        return JsonResponse(list(tickets), safe=False)
    return JsonResponse({'error': 'Invalid request.'}, status=400)

# Ticket View for Administrators in their Dashboard
def admin_view_tickets(request):
    """
    Retrieves and returns a JSON response containing all tickets for administrators.

    Only accessible to staff users. Administrators can optionally filter tickets by status 
    and sort them by a specified field. The default sorting is by the creation date.

    :param request: The request object containing optional query parameters 'sort_by' and 'status'.
    :return: A JsonResponse containing a list of tickets with their id, category, description, 
             created_at timestamp, status, and the username of the user who submitted the ticket.
             Returns a 403 error if the user is not a staff member.
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    sort_by = request.GET.get('sort_by', 'created_at')
    status_filter = request.GET.get('status', None)  # Optional status filter
    tickets = Ticket.objects.all()

    if status_filter:
        tickets = tickets.filter(status=status_filter)

    tickets = tickets.order_by(sort_by)
    ticket_data = tickets.values(
        'id', 'category', 'description', 'created_at', 'status', 'user__username'
    )
    
    return JsonResponse(list(ticket_data), safe=False)

# Administrator begins working on a ticket.
@csrf_exempt
@login_required
def update_ticket_status(request, ticket_id):
    """
    Handles a PATCH request to update the status of a specific ticket.

    Only accessible to staff users. The request body must contain the new status
    of the ticket in JSON format. The new status must be one of the valid choices
    for a Ticket object.

    :param request: The request object containing the new status of the ticket
    :param ticket_id: The id of the ticket to be updated
    :return: A JsonResponse containing a success message and the new status of the
             ticket if the update is successful. Returns a 403 error if the user
             is not a staff member, a 404 error if the ticket does not exist, a
             400 error if the request body is invalid JSON, and a 400 error if the
             new status is not one of the valid choices.
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        ticket = Ticket.objects.get(id=ticket_id)
        data = json.loads(request.body)
        new_status = data.get('status')

        if new_status not in dict(Ticket.STATUS_CHOICES):
            return JsonResponse({'error': 'Invalid status'}, status=400)
        

        if new_status == "closed":
            notifs = Notification.objects.filter(info=ticket.id)
            for notif in notifs:
                notif.delete()
            
            # create a notification to notify the user that their ticket was closed
            Notification.objects.create(
            user = ticket.user,
            info = f"{ticket.id}",
            header = "Issue closed",
            message = f"Your {ticket.category} issue has been marked as closed"
        )
        if new_status == "in_progress":
            notifs = Notification.objects.filter(info=ticket.id)
            for notif in notifs:
                notif.delete()
            
            # create a notification to notify the user that their ticket was in progress
            Notification.objects.create(
            user = ticket.user,
            info = f"{ticket.id}",
            header = f"Your ticket {ticket.id} in progress",
            message = f"Your {ticket.category} issue has been marked as in progress"
        )

        ticket.status = new_status
        ticket.save()
        return JsonResponse({'success': True, 'status': ticket.status})

    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'Ticket not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

# Administrator marks a ticket as completed.
@csrf_exempt
@login_required
def complete_ticket(request, ticket_id):
    """
    Handles a PATCH request to mark a specific ticket as completed.

    Only accessible to staff users. If the ticket does not exist, returns a 404 error.

    :param request: The request object
    :param ticket_id: The id of the ticket to be marked as completed
    :return: A JsonResponse containing a success message if the update is successful.
             Returns a 403 error if the user is not a staff member and a 404 error
             if the ticket does not exist.
    """

    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.completed = True
        ticket.save()

        return JsonResponse({'success': True})
    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'Ticket not found'}, status=404)

@login_required
def update_account(request):
    """
    Handles a POST request to update the user's account details.

    Only accessible to logged in users. If the request method is not POST, returns a 400 error.

    The request must contain the following fields in the JSON body:
        - first_name: The new first name.
        - last_name: The new last name.
        - email: The new email address.
        - current_password: The current password to verify.
        - new_password (optional): The new password to set.

    Returns a JsonResponse containing a success message if the update is successful.
    Returns a 400 error if the request is not a POST request or if the current password is incorrect.
    """
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
    """
    Returns a JsonResponse containing user information for pre-filling the update account form.

    Returns a 400 error if the request is not a GET request.
    """
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
    
    """
    Returns a JsonResponse containing the user's notifications, either read or unread depending on the load_type parameter.

    The request must be a GET request. If the request is not a GET request or if load_type is not 'read' or 'unread', returns a 400 error.

    The JsonResponse contains a list of notifications, each notification being a dictionary with the following fields:
        - id: The notification's id.
        - header: The notification's header.
        - message: The notification's message.
        - time_created: The notification's time of creation.
        - is_archived: Whether the notification is archived or not.
        - is_read: Whether the notification is read or not.

    :param request: The request object
    :param load_type: The type of notifications to load. Must be 'read' or 'unread'.
    :return: A JsonResponse containing the user's notifications
    """
    if request.method == 'GET':
        if load_type != 'read' and load_type != 'unread':
            return JsonResponse({'error': 'Invalid request'}, status=400)
        
        if load_type == 'read':
            notifications = Notification.objects.filter(user=request.user, is_archived=False, is_read=True).values('id','header', 'message', 'time_created', 'is_archived','is_read').order_by('-time_created')
        elif load_type == 'unread':
            notifications = Notification.objects.filter(user=request.user, is_archived=False, is_read=False).values('id','header', 'message', 'time_created', 'is_archived').order_by('-time_created')
        data = {
            "notifications": list(notifications),
        }
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def dismiss_notification(request, id):
    """
    Handles a PATCH request to dismiss a notification.

    The request must contain the id of the notification in the URL parameters.
    If the request is not a PATCH request or if the notification does not exist, returns a 400 error.

    :param request: The request object
    :param id: The id of the notification to be dismissed
    :return: A JsonResponse containing a success message if the update is successful.
             Returns a 400 error if the request is not a PATCH request or if the notification does not exist.
    """
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
    """
    Handles a PATCH request to mark a notification as read.

    The request must contain the id of the notification in the URL parameters.
    If the request is not a PATCH request or if the notification does not exist, returns a 400 error.

    :param request: The request object
    :param id: The id of the notification to be marked as read
    :return: A JsonResponse containing a success message if the update is successful.
             Returns a 400 error if the request is not a PATCH request or if the notification does not exist.
    """
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
    """
    Renders the error page when a test is invalidated or an error occurs.

    :param request: The HTTP request object
    :return: A rendered HttpResponse object for the error page
    """
    return render(request, 'errorpage.html')

def completionpage(request):
    """
    Renders the completion page when a test is completed.

    :param request: The HTTP request object
    :return: A rendered HttpResponse object for the completion page
    """
    return render(request, 'completionpage.html')

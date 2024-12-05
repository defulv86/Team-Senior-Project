from django.contrib.auth.models import User
from website.models import Ticket, Test, Notification, Aggregate, Response, Result, Stimulus, Stimulus_Type
from website.views import update_or_create_aggregate
from django.utils import timezone
from datetime import timedelta, datetime
from random import randint, choice, uniform, shuffle


# Delete existing records
User.objects.all().delete()
Test.objects.all().delete()
Ticket.objects.all().delete()
Notification.objects.all().delete()
Aggregate.objects.all().delete()
Response.objects.all().delete()
Result.objects.all().delete()
Stimulus.objects.all().delete()
Stimulus_Type.objects.all().delete()
# Create superuser 'admin' with password 'password'
admin_user = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')

# Create additional user 'DoctorWho' with password '@password115'
doctor_who = User.objects.create_user(username='DoctorWho', password='@password115')


# 2. Pending Test
pending_test = Test.objects.create(
	user=doctor_who,
	age=42,
	created_at=timezone.now(),
	status='pending'
)

# 3. Pending Test (Testing notification send out if the test has 24 hours left until expiration)
pending_test_2 = Test.objects.create(
	user=doctor_who,
	age=88,
	created_at=timezone.now() - timedelta(days=5, hours=23, minutes=59),
	status='pending'
)

# 4. Invalid Test (created 6 days, 23 hours, and 59 minutes ago. Testing to see if it updates when a minute passes)
invalid_test_1 = Test.objects.create(
	user=doctor_who,
	age=64,
	created_at=timezone.now() - timedelta(days=6, hours=23, minutes=59)
)

four_span_digit_type = Stimulus_Type.objects.create(stimulus_type='4_Span_Digit')
four_span_mixed_type = Stimulus_Type.objects.create(stimulus_type='4_Span_Mixed')
five_span_digit_type = Stimulus_Type.objects.create(stimulus_type='5_Span_Digit')
five_span_mixed_type = Stimulus_Type.objects.create(stimulus_type='5_Span_Mixed')
four_span_digit_type_pr = Stimulus_Type.objects.create(stimulus_type='4_Span_Digit_Pr')
four_span_mixed_type_pr = Stimulus_Type.objects.create(stimulus_type='4_Span_Mixed_Pr')
five_span_digit_type_pr = Stimulus_Type.objects.create(stimulus_type='5_Span_Digit_Pr')
five_span_mixed_type_pr = Stimulus_Type.objects.create(stimulus_type='5_Span_Mixed_Pr')


stimulus_instance_1 = Stimulus.objects.create(
	stimulus_content = "6254",
	stimulus_type = four_span_digit_type_pr  # Assigning the actual instance here
)

stimulus_instance_2 = Stimulus.objects.create(
	stimulus_content = "46523",
	stimulus_type = five_span_digit_type_pr
)

stimulus_instance_3 = Stimulus.objects.create(
	stimulus_content = "2463",
	stimulus_type = four_span_digit_type
)

stimulus_instance_4 = Stimulus.objects.create(
	stimulus_content = "6135",
	stimulus_type = four_span_digit_type
)

stimulus_instance_5 = Stimulus.objects.create(
	stimulus_content = "4125",
	stimulus_type = four_span_digit_type
)

stimulus_instance_6 = Stimulus.objects.create(
	stimulus_content = "43512",
	stimulus_type = five_span_digit_type
)

stimulus_instance_7 = Stimulus.objects.create(
	stimulus_content = "53416",
	stimulus_type = five_span_digit_type
)

stimulus_instance_8 = Stimulus.objects.create(
	stimulus_content = "45231",
	stimulus_type = five_span_digit_type
)

stimulus_instance_9 = Stimulus.objects.create(
	stimulus_content = "6R5K",
	stimulus_type = four_span_mixed_type_pr
)

stimulus_instance_10 = Stimulus.objects.create(
	stimulus_content = "4L6Y3",
	stimulus_type = five_span_mixed_type_pr
)

stimulus_instance_11 = Stimulus.objects.create(
	stimulus_content = "6F5P",
	stimulus_type = four_span_mixed_type
)

stimulus_instance_12 = Stimulus.objects.create(
	stimulus_content = "5YR2",
	stimulus_type = four_span_mixed_type
)

stimulus_instance_13 = Stimulus.objects.create(
	stimulus_content = "P5L6",
	stimulus_type = four_span_mixed_type
)

stimulus_instance_14 = Stimulus.objects.create(
	stimulus_content = "31RF4",
	stimulus_type = five_span_mixed_type
)

stimulus_instance_15 = Stimulus.objects.create(
	stimulus_content = "L361Y",
	stimulus_type = five_span_mixed_type
)

stimulus_instance_16 = Stimulus.objects.create(
	stimulus_content="62K4P",
	stimulus_type = five_span_mixed_type
)

# Create a Ticket instance submitted by DoctorWho
Ticket.objects.create(
	user=doctor_who,
	category='general',
	description="This is a sample issue reported by DoctorWho.",
	created_at=timezone.now(),
	status='open'  # Set the default or desired status
)


# Stimuli contents mapped to their instances
stimuli_contents = {
	1: "6254", 2: "46523", 3: "2463", 4: "6135", 5: "4125",
	6: "43512", 7: "53416", 8: "45231", 9: "6R5K", 10: "4L6Y3",
	11: "6F5P", 12: "5YR2", 13: "P5L6", 14: "31RF4", 15: "L361Y", 16: "62K4P"
}

# Helper functions for response generation
def generate_random_response(stimulus: str) -> str:
    """
    Generate a randomized response based on the stimulus:
    - Digits-only stimuli: digits are shuffled.
    - Mixed stimuli: digits and letters are shuffled separately.
    """
    digits = [ch for ch in stimulus if ch.isdigit()]
    letters = [ch for ch in stimulus if ch.isalpha()]
    shuffle(digits)
    shuffle(letters)
    return "".join(digits + letters)

def generate_ordered_response(stimulus: str) -> str:
    """
    Generate the correct response based on the stimulus:
    - Digits-only stimuli: digits are sorted in ascending order.
    - Mixed stimuli: digits in ascending order, followed by letters in ascending order.
    """
    digits = sorted(ch for ch in stimulus if ch.isdigit())
    letters = sorted(ch for ch in stimulus if ch.isalpha())
    return "".join(digits + letters)

def calculate_character_accuracy(response: str, stimulus: str) -> list[int]:
    """
    Compare the response to the stimulus based on the expected sorted order.

    A value of 1 is given **only if the character in the response matches the
    character in the exact position of the expected sorted order**.
    """
    # Get the expected sorted order of the stimulus
    expected_order = ''.join(sorted(stimulus))
    # Pad the response to match the stimulus length if shorter
    response = response.ljust(len(stimulus))
    # Compare each character in the response to the expected order
    accuracy = [
        1 if response[i] == expected_order[i] else 0
        for i in range(len(expected_order))
    ]
    return accuracy

def is_correct_order(response: str, stimulus: str) -> bool:
    """
    Check if the response matches the correct ordering of the stimulus:
    - For digits-only stimuli: ascending order of digits.
    - For mixed stimuli: digits in ascending order, then letters in ascending order.
    """
    expected_order = generate_ordered_response(stimulus)
    return response == expected_order


# Define age groups
age_groups = [(18, 29), (30, 39), (40, 49), (50, 59), (60, 69), (70, 79), (80, 89), (90, 99)]

# Store generated data
tests_data = []
results_data = []
responses_data = []
aggregate_data = []

# Generate data for each age group
for min_age, max_age in age_groups:
	avg_latencies = {str(i): [] for i in range(1, 17)}
	avg_accuracies = {str(i): [] for i in range(1, 17)}
	for test_num in range(9):
		age = randint(min_age, max_age)
		created_at = timezone.now() - timedelta(days=randint(1, 6))
		started_at = created_at + timedelta(minutes=randint(1, 60))
		finished_at = started_at + timedelta(minutes=randint(5, 15))
		test_instance = Test.objects.create(
			user=doctor_who,
			age=age,
			created_at=created_at,
			started_at=started_at,
			finished_at=finished_at,
			status="completed"
		)
		character_latencies = {}
		character_accuracies = {}
		amount_correct = 0
		test_start_time = started_at
		for i in range(1, 17):
			stimulus_content = stimuli_contents[i]
			response = generate_random_response(stimulus_content)  # Randomized patient response
			expected_order = generate_ordered_response(stimulus_content)  # Correct sorted order
			if response == expected_order:
				accuracy = [1] * len(stimulus_content)  # Perfect match
				amount_correct += 1
			else:
				accuracy = calculate_character_accuracy(response, stimulus_content)  # Partial match
			character_accuracies[str(i)] = accuracy
			latencies = [round(uniform(500.0, 3000.0), 2) for _ in stimulus_content]
			character_latencies[str(i)] = latencies
			avg_latencies[str(i)].extend(latencies)
			avg_accuracies[str(i)].extend(accuracy)
			time_submitted = test_start_time + timedelta(seconds=randint(30, 90))
			test_start_time = time_submitted
			response_data = Response.objects.create(
				response=response,
				test=test_instance,
				response_position=i,
				stimulus=Stimulus.objects.get(stimulus_content=stimulus_content),
				time_submitted=time_submitted
			)
		result = Result.objects.create(
			test=test_instance,
			character_latencies=character_latencies,
			character_accuracies=character_accuracies,
			amount_correct=amount_correct
		)
		update_or_create_aggregate(test_instance)

# Output generated data
for test in tests_data:
	Test.objects.create(**test)

for result in results_data:
	Result.objects.create(**result)

for response in responses_data:
	Response.objects.create(**response)

for aggregate in aggregate_data:
	Aggregate.objects.create(**aggregate)



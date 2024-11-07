from django.contrib.auth.models import User
from website.models import Ticket, Test, Notification, Aggregate, Response, Result, Stimulus, Stimulus_Type
from django.utils import timezone
from datetime import timedelta, datetime

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

# Test instances:
# 1. Completed Test
completed_test = Test.objects.create(
    user=doctor_who,
    age=54,
    created_at=timezone.now() - timedelta(days=5),
    started_at=timezone.now() - timedelta(days=4),
    finished_at=timezone.now() - timedelta(days=4) + timedelta(minutes=20),
    status='completed'
)

# 2. Pending Test
pending_test = Test.objects.create(
    user=doctor_who,
    age=42,
    created_at=timezone.now(),
    status='pending'
)

# 3. Invalid Test (created a week ago, started but not completed)
invalid_test = Test.objects.create(
    user=doctor_who,
    age=67,
    created_at=timezone.now() - timedelta(days=10),
    started_at=timezone.now() - timedelta(days=9),
    status='invalid'
)

# Create a Ticket instance submitted by DoctorWho
Ticket.objects.create(
    user=doctor_who,
    category='general',
    description="This is a sample issue reported by DoctorWho.",
    created_at=timezone.now()
)

Notification.objects.create(
    user=doctor_who,
    test=invalid_test,
    header="Reminder: Patient Test Incomplete", 
    message="Patient test at ppst.com/testLink1 has not been taken yet. Please follow up.",
    time_created=datetime(2024, 10, 25, 9, 0, 0),
    is_dismissed=False,
    is_viewed=False
)


aggregates_data = [
    {
        "min_age": 50,
        "max_age": 59,
        "average_latencies": {
            "fourdigit_1": 140,
            "fourdigit_2": 150,
            "fourdigit_3": 160,
            "fivedigit_1": 190,
            "fivedigit_2": 175,
            "fivedigit_3": 190,
            "fourmixed_1": 120,
            "fourmixed_2": 155,
            "fourmixed_3": 125,
            "fivemixed_1": 185,
            "fivemixed_2": 195,
            "fivemixed_3": 200
        },
        "average_accuracies": {
            "fourdigit_1": 0.79,
            "fourdigit_2": 0.74,
            "fourdigit_3": 0.70,
            "fivedigit_1": 0.68,
            "fivedigit_2": 0.71,
            "fivedigit_3": 0.65,
            "fourmixed_1": 0.76,
            "fourmixed_2": 0.80,
            "fourmixed_3": 0.84,
            "fivemixed_1": 0.65,
            "fivemixed_2": 0.71,
            "fivemixed_3": 0.72
        }
    },
    # Add more dictionaries for other age groups as needed
]

for aggregate_data in aggregates_data:
    Aggregate.objects.create(**aggregate_data)




# Results data
results_data = [
    {
        "test": completed_test,
        "character_latencies": {0: [150, 140, 130], 1: [160, 155, 150], 2: [140, 135, 130]},  # Example latencies by position
        "character_accuracies": {0: [1, 0, 1], 1: [1, 1, 0], 2: [0, 1, 1]},  # Example accuracies by position
        "amount_correct": 10
    }
]

for result_data in results_data:
    Result.objects.create(**result_data)

# Create Stimulus_Type instances
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
    stimulus_content = "6R5K",
    stimulus_type = four_span_mixed_type_pr
)

stimulus_instance_4 = Stimulus.objects.create(
    stimulus_content = "4L6Y3",
    stimulus_type = five_span_mixed_type_pr
)

stimulus_instance_5 = Stimulus.objects.create(
    stimulus_content = "2463",
    stimulus_type = four_span_digit_type
)

stimulus_instance_6 = Stimulus.objects.create(
    stimulus_content = "6135",
    stimulus_type = four_span_digit_type
)

stimulus_instance_7 = Stimulus.objects.create(
    stimulus_content = "4125",
    stimulus_type = four_span_digit_type
)

stimulus_instance_8 = Stimulus.objects.create(
    stimulus_content = "43512",
    stimulus_type = five_span_digit_type
)

stimulus_instance_9 = Stimulus.objects.create(
    stimulus_content = "53416",
    stimulus_type = five_span_digit_type
)

stimulus_instance_10 = Stimulus.objects.create(
    stimulus_content = "45231",
    stimulus_type = five_span_digit_type
)

stimulus_instance_11 = Stimulus.objects.create(
    stimulus_content = "6F5P",
    stimulus_type = four_span_mixed_type
)

stimulus_instance_12 = Stimulus.objects.create(
    stimulus_content = "5Y42",
    stimulus_type = four_span_mixed_type
)

stimulus_instance_13 = Stimulus.objects.create(
    stimulus_content = "P5L8",
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
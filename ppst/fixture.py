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

# Notifications for admin_user
Notification.objects.create(
    user=doctor_who,
    header="Reminder: Patient Test Incomplete", 
    message="Patient test at ppst.com/testLink1 has not been taken yet. Please follow up.",
    time_created=datetime(2024, 10, 25, 9, 0, 0),
    is_dismissed=False
)


# Aggregates data
aggregates_data = [
    {"min_age": 50, "max_age": 59, "avg_fourdigit_accuracy_1": 0.79, "avg_fourdigit_latency_1": 140, "avg_fourdigit_accuracy_2": 0.74, "avg_fourdigit_latency_2": 150, "avg_fourdigit_accuracy_3": 0.70, "avg_fourdigit_latency_3": 160, "avg_fivedigit_accuracy_1": 0.68, "avg_fivedigit_latency_1": 190, "avg_fivedigit_accuracy_2": 0.71, "avg_fivedigit_latency_2": 175, "avg_fivedigit_accuracy_3": 0.65, "avg_fivedigit_latency_3": 190, "avg_fourmixed_accuracy_1": 0.76, "avg_fourmixed_latency_1": 120, "avg_fourmixed_accuracy_2": 0.80, "avg_fourmixed_latency_2": 155, "avg_fourmixed_accuracy_3": 0.84, "avg_fourmixed_latency_3": 125, "avg_fivemixed_accuracy_1": 0.65, "avg_fivemixed_latency_1": 185, "avg_fivemixed_accuracy_2": 0.71, "avg_fivemixed_latency_2": 195, "avg_fivemixed_accuracy_3": 0.72, "avg_fivemixed_latency_3": 200},
    {"min_age": 60, "max_age": 69, "avg_fourdigit_accuracy_1": 0.75, "avg_fourdigit_latency_1": 150, "avg_fourdigit_accuracy_2": 0.68, "avg_fourdigit_latency_2": 160, "avg_fourdigit_accuracy_3": 0.72, "avg_fourdigit_latency_3": 155, "avg_fivedigit_accuracy_1": 0.65, "avg_fivedigit_latency_1": 200, "avg_fivedigit_accuracy_2": 0.70, "avg_fivedigit_latency_2": 180, "avg_fivedigit_accuracy_3": 0.67, "avg_fivedigit_latency_3": 190, "avg_fourmixed_accuracy_1": 0.80, "avg_fourmixed_latency_1": 140, "avg_fourmixed_accuracy_2": 0.78, "avg_fourmixed_latency_2": 145, "avg_fourmixed_accuracy_3": 0.82, "avg_fourmixed_latency_3": 135, "avg_fivemixed_accuracy_1": 0.60, "avg_fivemixed_latency_1": 210, "avg_fivemixed_accuracy_2": 0.63, "avg_fivemixed_latency_2": 205, "avg_fivemixed_accuracy_3": 0.62, "avg_fivemixed_latency_3": 215},
    {"min_age": 70, "max_age": 79, "avg_fourdigit_accuracy_1": 0.70, "avg_fourdigit_latency_1": 160, "avg_fourdigit_accuracy_2": 0.65, "avg_fourdigit_latency_2": 170, "avg_fourdigit_accuracy_3": 0.69, "avg_fourdigit_latency_3": 165, "avg_fivedigit_accuracy_1": 0.58, "avg_fivedigit_latency_1": 220, "avg_fivedigit_accuracy_2": 0.62, "avg_fivedigit_latency_2": 215, "avg_fivedigit_accuracy_3": 0.60, "avg_fivedigit_latency_3": 225, "avg_fourmixed_accuracy_1": 0.75, "avg_fourmixed_latency_1": 155, "avg_fourmixed_accuracy_2": 0.77, "avg_fourmixed_latency_2": 150, "avg_fourmixed_accuracy_3": 0.74, "avg_fourmixed_latency_3": 160, "avg_fivemixed_accuracy_1": 0.55, "avg_fivemixed_latency_1": 230, "avg_fivemixed_accuracy_2": 0.57, "avg_fivemixed_latency_2": 240, "avg_fivemixed_accuracy_3": 0.54, "avg_fivemixed_latency_3": 235}
]

for aggregate_data in aggregates_data:
    Aggregate.objects.create(**aggregate_data)




results_data = [
    {
        "test": completed_test, 
        "fourdigit_accuracy_1": 0.82, "fourdigit_latency_1": 130,
        "fourdigit_accuracy_2": 0.78, "fourdigit_latency_2": 140,
        "fourdigit_accuracy_3": 0.75, "fourdigit_latency_3": 150,
        "fivedigit_accuracy_1": 0.69, "fivedigit_latency_1": 185,
        "fivedigit_accuracy_2": 0.73, "fivedigit_latency_2": 165,
        "fivedigit_accuracy_3": 0.68, "fivedigit_latency_3": 180,
        "fourmixed_accuracy_1": 0.79, "fourmixed_latency_1": 115,
        "fourmixed_accuracy_2": 0.81, "fourmixed_latency_2": 145,
        "fourmixed_accuracy_3": 0.85, "fourmixed_latency_3": 130,
        "fivemixed_accuracy_1": 0.67, "fivemixed_latency_1": 180,
        "fivemixed_accuracy_2": 0.74, "fivemixed_latency_2": 190,
        "fivemixed_accuracy_3": 0.73, "fivemixed_latency_3": 195,
        "amount_correct": 10  # Set within the range of actual test questions
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
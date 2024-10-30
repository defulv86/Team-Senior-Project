from django.contrib.auth.models import User
from website.models import Ticket, Test, Notification, Aggreagate, Response, Result, Stimulus, Stimulus_Type
from django.utils import timezone
from datetime import datetime

# Delete existing records
User.objects.all().delete()
Test.objects.all().delete()
Ticket.objects.all().delete()
Notification.objects.all().delete()
Aggreagate.objects.all().delete()
Response.objects.all().delete()
Result.objects.all().delete()
Stimulus.objects.all().delete()
Stimulus_Type.objects.all().delete()
# Create superuser 'admin' with password 'password'
admin_user = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')

# Create additional user 'DoctorWho' with password '@password115'
doctor_who = User.objects.create_user(username='DoctorWho', password='@password115')

# Create a Test instance associated with DoctorWho
test_instance = Test.objects.create(
    user=doctor_who,
    age=35,  # Example age, adjust as needed
    created_at=timezone.now()
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
    {"age_group": "50-60", "avg_fourdigit_accuracy_1": 0.0, "avg_fourdigit_latency_1": 0, "avg_fourdigit_accuracy_2": 0.0, "avg_fourdigit_latency_2": 0, "avg_fourdigit_accuracy_3": 0.0, "avg_fourdigit_latency_3": 0, "avg_fivedigit_accuracy_1": 0.0, "avg_fivedigit_latency_1": 0, "avg_fivedigit_accuracy_2": 0.0, "avg_fivedigit_latency_2": 0, "avg_fivedigit_accuracy_3": 0.0, "avg_fivedigit_latency_3": 0, "avg_fourmixed_accuracy_1": 0.0, "avg_fourmixed_latency_1": 0, "avg_fourmixed_accuracy_2": 0.0, "avg_fourmixed_latency_2": 0, "avg_fourmixed_accuracy_3": 0.0, "avg_fourmixed_latency_3": 0, "avg_fivemixed_accuracy_1": 0.0, "avg_fivemixed_latency_1": 0, "avg_fivemixed_accuracy_2": 0.0, "avg_fivemixed_latency_2": 0, "avg_fivemixed_accuracy_3": 0.0, "avg_fivemixed_latency_3": 0},
    {"age_group": "60-70", "avg_fourdigit_accuracy_1": 0.75, "avg_fourdigit_latency_1": 150, "avg_fourdigit_accuracy_2": 0.68, "avg_fourdigit_latency_2": 160, "avg_fourdigit_accuracy_3": 0.72, "avg_fourdigit_latency_3": 155, "avg_fivedigit_accuracy_1": 0.65, "avg_fivedigit_latency_1": 200, "avg_fivedigit_accuracy_2": 0.70, "avg_fivedigit_latency_2": 180, "avg_fivedigit_accuracy_3": 0.67, "avg_fivedigit_latency_3": 190, "avg_fourmixed_accuracy_1": 0.80, "avg_fourmixed_latency_1": 140, "avg_fourmixed_accuracy_2": 0.78, "avg_fourmixed_latency_2": 145, "avg_fourmixed_accuracy_3": 0.82, "avg_fourmixed_latency_3": 135, "avg_fivemixed_accuracy_1": 0.60, "avg_fivemixed_latency_1": 210, "avg_fivemixed_accuracy_2": 0.63, "avg_fivemixed_latency_2": 205, "avg_fivemixed_accuracy_3": 0.62, "avg_fivemixed_latency_3": 215},
    {"age_group": "70-80", "avg_fourdigit_accuracy_1": 0.70, "avg_fourdigit_latency_1": 160, "avg_fourdigit_accuracy_2": 0.65, "avg_fourdigit_latency_2": 170, "avg_fourdigit_accuracy_3": 0.69, "avg_fourdigit_latency_3": 165, "avg_fivedigit_accuracy_1": 0.58, "avg_fivedigit_latency_1": 220, "avg_fivedigit_accuracy_2": 0.62, "avg_fivedigit_latency_2": 215, "avg_fivedigit_accuracy_3": 0.60, "avg_fivedigit_latency_3": 225, "avg_fourmixed_accuracy_1": 0.75, "avg_fourmixed_latency_1": 155, "avg_fourmixed_accuracy_2": 0.77, "avg_fourmixed_latency_2": 150, "avg_fourmixed_accuracy_3": 0.74, "avg_fourmixed_latency_3": 160, "avg_fivemixed_accuracy_1": 0.55, "avg_fivemixed_latency_1": 230, "avg_fivemixed_accuracy_2": 0.57, "avg_fivemixed_latency_2": 240, "avg_fivemixed_accuracy_3": 0.54, "avg_fivemixed_latency_3": 235}
]

for aggregate_data in aggregates_data:
    Aggreagate.objects.create(**aggregate_data)


# Results data
results_data = [
    {"test": test_instance, "fourdigit_accuracy_1": 0.0, "fourdigit_latency_1": 0, "fourdigit_accuracy_2": 0.0, "fourdigit_latency_2": 0, "fourdigit_accuracy_3": 0.0, "fourdigit_latency_3": 0, "fivedigit_accuracy_1": 0.0, "fivedigit_latency_1": 0, "fivedigit_accuracy_2": 0.0, "fivedigit_latency_2": 0, "fivedigit_accuracy_3": 0.0, "fivedigit_latency_3": 0, "fourmixed_accuracy_1": 0.0, "fourmixed_latency_1": 0, "fourmixed_accuracy_2": 0.0, "fourmixed_latency_2": 0, "fourmixed_accuracy_3": 0.0, "fourmixed_latency_3": 0, "fivemixed_accuracy_1": 0.0, "fivemixed_latency_1": 0, "fivemixed_accuracy_2": 0.0, "fivemixed_latency_2": 0, "fivemixed_accuracy_3": 0.0, "fivemixed_latency_3": 0, "amount_correct": 0},
    # Additional results based on result.json data...
]

# Results data from JSON
results_data = [
    {"test": test_instance, "fourdigit_accuracy_1": 0.0, "fourdigit_latency_1": 0, "fourdigit_accuracy_2": 0.0, "fourdigit_latency_2": 0, "fourdigit_accuracy_3": 0.0, "fourdigit_latency_3": 0, "fivedigit_accuracy_1": 0.0, "fivedigit_latency_1": 0, "fivedigit_accuracy_2": 0.0, "fivedigit_latency_2": 0, "fivedigit_accuracy_3": 0.0, "fivedigit_latency_3": 0, "fourmixed_accuracy_1": 0.0, "fourmixed_latency_1": 0, "fourmixed_accuracy_2": 0.0, "fourmixed_latency_2": 0, "fourmixed_accuracy_3": 0.0, "fourmixed_latency_3": 0, "fivemixed_accuracy_1": 0.0, "fivemixed_latency_1": 0, "fivemixed_accuracy_2": 0.0, "fivemixed_latency_2": 0, "fivemixed_accuracy_3": 0.0, "fivemixed_latency_3": 0, "amount_correct": 0},
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
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
    finished_at=timezone.now() - timedelta(days=4) + timedelta(minutes=4),
    status='completed'
)

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



# Create a Ticket instance submitted by DoctorWho
Ticket.objects.create(
    user=doctor_who,
    category='general',
    description="This is a sample issue reported by DoctorWho.",
    created_at=timezone.now()
)

Notification.objects.create(
    user=doctor_who,
    test=invalid_test_1,
    header="Reminder: Patient Test Incomplete", 
    message="Patient test at ppst.com/testLink1 has not been taken yet. Please follow up.",
    time_created=datetime(2024, 10, 25, 9, 0, 0),
    is_archived=False,
    is_read=False
)


aggregates_data = [
    {
        "min_age": 50,
        "max_age": 59,
        "average_latencies": {
            "fourdigit_1": 753,
            "fourdigit_2": 1331,
            "fourdigit_3": 969,
            "fivedigit_1": 1246.2,
            "fivedigit_2": 913,
            "fivedigit_3": 765.6,
            "fourmixed_1": 1619,
            "fourmixed_2": 1601.5,
            "fourmixed_3": 1395,
            "fivemixed_1": 1110.8,
            "fivemixed_2": 1744.4,
            "fivemixed_3": 1608.4
        },
        "average_accuracies": {
            "fourdigit_1": 1.0,
            "fourdigit_2": 1.0,
            "fourdigit_3": 1.0,
            "fivedigit_1": 1.0,
            "fivedigit_2": 1.0,
            "fivedigit_3": 1.0,
            "fourmixed_1": 1.0,
            "fourmixed_2": 1.0,
            "fourmixed_3": 1.0,
            "fivemixed_1": 1.0,
            "fivemixed_2": 0.8,
            "fivemixed_3": 1.0
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
        "character_latencies": {
            "1": [1246.0, 399.0, 706.0, 530.0],
            "2": [891.0, 1014.0, 750.0, 598.0, 643.0],
            "3": [1079.0, 395.0, 713.0, 825.0],
            "4": [1197.0, 762.0, 1902.0, 1463.0],
            "5": [1703.0, 485.0, 965.0, 723.0],
            "6": [1583.0, 2875.0, 597.0, 595.0, 581.0],
            "7": [1799.0, 882.0, 656.0, 439.0, 789.0],
            "8": [1212.0, 688.0, 614.0, 789.0, 525.0],
            "9": [2184.0, 1135.0, 687.0, 738.0],
            "10": [2057.0, 692.0, 1022.0, 684.0, 1115.0],
            "11": [1949.0, 1792.0, 1774.0, 961.0],
            "12": [3002.0, 925.0, 1689.0, 790.0],
            "13": [3158.0, 1144.0, 894.0, 384.0],
            "14": [1781.0, 784.0, 1738.0, 554.0, 697.0],
            "15": [1470.0, 3219.0, 1289.0, 2103.0, 641.0],
            "16": [1069.0, 842.0, 1069.0, 3657.0, 1405.0]
        },
        "character_accuracies": {
            "1": [1.0, 1.0, 1.0, 1.0],
            "2": [1.0, 1.0, 1.0, 1.0, 1.0],
            "3": [1.0, 1.0, 1.0, 1.0],
            "4": [1.0, 1.0, 1.0, 1.0],
            "5": [1.0, 1.0, 1.0, 1.0],
            "6": [1.0, 1.0, 1.0, 1.0, 1.0],
            "7": [1.0, 1.0, 1.0, 1.0, 1.0],
            "8": [1.0, 1.0, 1.0, 1.0, 1.0],
            "9": [1.0, 1.0, 1.0, 1.0],
            "10": [1.0, 1.0, 1.0, 1.0, 1.0],
            "11": [1.0, 1.0, 1.0, 1.0],
            "12": [1.0, 1.0, 1.0, 1.0],
            "13": [1.0, 1.0, 1.0, 1.0],
            "14": [1.0, 1.0, 1.0, 1.0, 1.0],
            "15": [1.0, 1.0, 1.0, 1.0, 0.0],
            "16": [1.0, 1.0, 1.0, 1.0, 1.0]
        },
        "amount_correct": 15  # Adjust this based on the correct responses as needed
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


test_response_1 = [
    {
        "response": "2456",
        "test": completed_test,
        "response_position": 1,
        "stimulus": stimulus_instance_1,
        "time_submitted": "2024-10-25T11:00:00.000Z"
    }
]
for test_response_1 in test_response_1:
    Response.objects.create(**test_response_1)

test_response_2 = [
    {
        "response": "23456",
        "test": completed_test,
        "response_position": 2,
        "stimulus": stimulus_instance_2,
        "time_submitted": "2024-10-25T11:05:00.000Z"
    }
]
for test_response_2 in test_response_2:
    Response.objects.create(**test_response_2)

test_response_3 = [
    {
        "response": "2346",
        "test": completed_test,
        "response_position": 3,
        "stimulus": stimulus_instance_3,
        "time_submitted": "2024-10-25T11:10:00.000Z"
    }
]
for test_response_3 in test_response_3:
    Response.objects.create(**test_response_3)

test_response_4 = [
    {
        "response": "1356",
        "test": completed_test,
        "response_position": 4,
        "stimulus": stimulus_instance_4,
        "time_submitted": "2024-10-25T11:15:00.000Z"
    }
]
for test_response_4 in test_response_4:
    Response.objects.create(**test_response_4)

test_response_5 = [
    {
        "response": "1245",
        "test": completed_test,
        "response_position": 5,
        "stimulus": stimulus_instance_5,
        "time_submitted": "2024-10-25T11:20:00.000Z"
    }
]
for test_response_5 in test_response_5:
    Response.objects.create(**test_response_5)

test_response_6 = [
    {
        "response": "2456",
        "test": completed_test,
        "response_position": 6,
        "stimulus": stimulus_instance_6,
        "time_submitted": "2024-10-25T11:25:00.000Z"
    }
]
for test_response_6 in test_response_6:
    Response.objects.create(**test_response_6)

test_response_7 = [
    {
        "response": "13456",
        "test": completed_test,
        "response_position": 7,
        "stimulus": stimulus_instance_7,
        "time_submitted": "2024-10-25T11:30:00.000Z"
    }
]
for test_response_7 in test_response_7:
    Response.objects.create(**test_response_7)

test_response_8 = [
    {
        "response": "13456",
        "test": completed_test,
        "response_position": 8,
        "stimulus": stimulus_instance_8,
        "time_submitted": "2024-10-25T11:35:00.000Z"
    }
]
for test_response_8 in test_response_8:
    Response.objects.create(**test_response_8)

test_response_9 = [
    {
        "response": "56RK",
        "test": completed_test,
        "response_position": 9,
        "stimulus": stimulus_instance_9,
        "time_submitted": "2024-10-25T11:40:00.000Z"
    }
]
for test_response_9 in test_response_9:
    Response.objects.create(**test_response_9)

test_response_10 = [
    {
        "response": "346LY",
        "test": completed_test,
        "response_position": 10,
        "stimulus": stimulus_instance_10,
        "time_submitted": "2024-10-25T11:45:00.000Z"
    }
]
for test_response_10 in test_response_10:
    Response.objects.create(**test_response_10)

test_response_11 = [
    {
        "response": "56FP",
        "test": completed_test,
        "response_position": 11,
        "stimulus": stimulus_instance_11,
        "time_submitted": "2024-10-25T11:50:00.000Z"
    }
]
for test_response_11 in test_response_11:
    Response.objects.create(**test_response_11)

test_response_12 = [
    {
        "response": "25RY",
        "test": completed_test,
        "response_position": 12,
        "stimulus": stimulus_instance_12,
        "time_submitted": "2024-10-25T11:55:00.000Z"
    }
]
for test_response_12 in test_response_12:
    Response.objects.create(**test_response_12)

test_response_13 = [
    {
        "response": "56LP",
        "test": completed_test,
        "response_position": 13,
        "stimulus": stimulus_instance_13,
        "time_submitted": "2024-10-25T12:00:00.000Z"
    }
]
for test_response_13 in test_response_13:
    Response.objects.create(**test_response_13) 

test_response_14 = [
    {
        "response": "134FR",
        "test": completed_test,
        "response_position": 14,
        "stimulus": stimulus_instance_14,
        "time_submitted": "2024-10-25T12:05:00.000Z"
    }
]
for test_response_14 in test_response_14:
    Response.objects.create(**test_response_14)

test_response_15 = [
    {
        "response": "136LP",
        "test": completed_test,
        "response_position": 15,
        "stimulus": stimulus_instance_15,
        "time_submitted": "2024-10-25T12:10:00.000Z"
    }
]
for test_response_15 in test_response_15:
    Response.objects.create(**test_response_15)

test_response_16 = [
    {
        "response": "246KP",
        "test": completed_test,
        "response_position": 16,
        "stimulus": stimulus_instance_16,
        "time_submitted": "2024-10-25T12:15:00.000Z"
    }
]
for test_response_16 in test_response_16:
    Response.objects.create(**test_response_16)



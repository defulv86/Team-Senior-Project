from django.contrib.auth.models import User
from website.models import Ticket, Test, Notification, Aggregate, Response, Result, Stimulus, Stimulus_Type
from website.views import update_or_create_aggregate
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

completed_test_2 = Test.objects.create(
    user=doctor_who,
    age=48,
    created_at=timezone.now() - timedelta(minutes=30),
    started_at=timezone.now() - timedelta(minutes=24),
    finished_at=timezone.now() - timedelta(minutes=15),
    status='completed'
)


completed_test_3 = Test.objects.create(
    user=doctor_who,
    age=45,
    created_at=timezone.now() - timedelta(minutes=50),
    started_at=timezone.now() - timedelta(minutes=45),
    finished_at=timezone.now() - timedelta(minutes=37 ),
    status='completed'
)

completed_test_4 = Test.objects.create(
    user=doctor_who,
    age=47,
    created_at=timezone.now() - timedelta(minutes=45),
    started_at=timezone.now() - timedelta(minutes=40),
    finished_at=timezone.now() - timedelta(minutes=30),
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
    created_at=timezone.now(),
    status='open'  # Set the default or desired status
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
    # Existing entry for age group 50-59
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
    # New entry for age group 40-49
    {
        "min_age": 40,
        "max_age": 49,
        "average_latencies": {
            "fourdigit_1": 1786.55,
            "fourdigit_2": 1464.22,
            "fourdigit_3": 1057.03,
            "fivedigit_1": 1280.04,
            "fivedigit_2": 1060.78,
            "fivedigit_3": 1133.62,
            "fourmixed_1": 1417.53,
            "fourmixed_2": 1552.5,
            "fourmixed_3": 1487.47,
            "fivemixed_1": 2298.44,
            "fivemixed_2": 2232.94,
            "fivemixed_3": 2129.44
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
            "fivemixed_1": 0.6,
            "fivemixed_2": 0.8,
            "fivemixed_3": 0.4
        }
    }
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
    },
    # New entry for completed_test_2
    {
        "test": completed_test_2,
        "character_latencies": {
            "1": [3213.5, 1334.5, 1140.1],
            "2": [2149.6, 1204.9, 1376.3, 1251.8, 965.4],
            "3": [3257.0, 1182.6, 1582.7, 1123.9],
            "4": [2363.6, 1142.3, 1188.9, 1162.1],
            "5": [1397.5, 826.0, 815.7, 1188.9],
            "6": [2164.4, 934.2, 1098.9, 1110.9, 1091.8],
            "7": [1252.0, 1035.7, 1094.8, 910.5, 1010.9],
            "8": [1439.7, 924.9, 1167.6, 1158.1, 977.8],
            "9": [3659.8, 2147.4, 878.3, 1420.7],
            "10": [6415.1, 999.6, 965.2, 1800.1, 1014.3],
            "11": [2425.6, 1282.7, 1109.9, 851.9],
            "12": [2069.0, 1006.9, 2032.9, 1101.2],
            "13": [2861.6, 1111.6, 1001.0, 975.7],
            "14": [1851.0, 955.4, 1189.7, 6336.7, 1159.4],
            "15": [2418.5, 962.3, 1162.3, 5496.0, 1125.6],
            "16": [3621.9, 1218.5, 1185.4, 3793.4, 828.0]
        },
        "character_accuracies": {
            "1": [0.0, 0.0, 0.0, 0.0],
            "2": [0.0, 0.0, 0.0, 0.0, 0.0],
            "3": [1.0, 1.0, 1.0, 1.0],
            "4": [1.0, 1.0, 1.0, 1.0],
            "5": [1.0, 1.0, 1.0, 1.0],
            "6": [1.0, 1.0, 1.0, 1.0, 1.0],
            "7": [1.0, 1.0, 1.0, 1.0, 1.0],
            "8": [1.0, 1.0, 1.0, 1.0, 1.0],
            "9": [1.0, 0.0, 0.0, 0.0],
            "10": [1.0, 1.0, 1.0, 0.0, 1.0],
            "11": [1.0, 1.0, 1.0, 1.0],
            "12": [1.0, 1.0, 1.0, 1.0],
            "13": [1.0, 1.0, 1.0, 1.0],
            "14": [1.0, 1.0, 1.0, 0.0, 0.0],
            "15": [1.0, 1.0, 1.0, 0.0, 1.0],
            "16": [1.0, 0.0, 1.0, 0.0, 0.0]
        },
        "amount_correct": 9
    },
    {
        "test": completed_test_3,
        "character_latencies": {
            "1": [1050.2, 700.1, 920.5, 680.2],
            "2": [1280.1, 1200.9, 850.7, 780.2, 670.6],
            "3": [990.3, 770.4, 600.6, 1120.9],
            "4": [1450.1, 810.3, 790.2, 660.1],
            "5": [1100.2, 640.3, 720.3, 980.1],
            "6": [980.5, 1020.1, 880.2, 750.2, 720.7],
            "7": [1230.0, 1035.0, 880.4, 990.9, 940.5],
            "8": [1050.2, 890.0, 1065.3, 920.2, 1031.4],
            "9": [760.0, 820.0, 950.5, 1020.4],
            "10": [1500.0, 990.0, 1010.3, 1045.7, 968.3],
            "11": [920.0, 850.0, 790.2, 1015.9],
            "12": [1170.0, 1005.1, 980.8, 910.2],
            "13": [1055.3, 970.4, 940.9, 890.3],
            "14": [1330.5, 1110.0, 1060.0, 980.4, 984.2],
            "15": [1140.7, 1095.4, 1180.6, 1040.4, 923.1],
            "16": [920.1, 1030.6, 1150.9, 1175.5, 1079.2]
        },
        "character_accuracies": {
            "1": [1.0, 1.0, 1.0, 1.0],
            "2": [1.0, 1.0, 1.0, 0.0, 1.0],
            "3": [1.0, 1.0, 0.0, 1.0],
            "4": [1.0, 1.0, 1.0, 1.0],
            "5": [1.0, 1.0, 1.0, 1.0],
            "6": [1.0, 0.0, 1.0, 1.0, 0.0],
            "7": [1.0, 1.0, 1.0, 1.0, 1.0],
            "8": [1.0, 1.0, 1.0, 1.0, 0.0],
            "9": [1.0, 0.0, 1.0, 1.0],
            "10": [1.0, 1.0, 1.0, 0.0, 0.0],
            "11": [1.0, 1.0, 1.0, 1.0],
            "12": [1.0, 1.0, 1.0, 1.0],
            "13": [1.0, 1.0, 1.0, 1.0],
            "14": [1.0, 1.0, 1.0, 0.0, 0.0],
            "15": [1.0, 1.0, 1.0, 1.0, 1.0],
            "16": [1.0, 1.0, 1.0, 1.0, 1.0]
        },
        "amount_correct": 14
    },
    {
        "test": completed_test_4,
        "character_latencies": {
            "1": [990.2, 1150.1, 1070.4, 1220.0],
            "2": [1230.7, 1080.4, 1130.3, 1010.6, 963.2],
            "3": [1120.4, 880.5, 920.6, 1030.9],
            "4": [970.5, 1040.4, 870.2, 960.7],
            "5": [910.1, 1020.2, 1150.3, 1100.2],
            "6": [1030.0, 930.2, 860.0, 1060.1, 1022.4],
            "7": [940.4, 990.9, 980.4, 890.6, 912.0],
            "8": [1170.2, 1020.4, 910.6, 960.9, 999.2],
            "9": [980.8, 990.2, 1040.8, 1010.5],
            "10": [910.2, 1130.1, 980.4, 1020.8, 1271.9],
            "11": [930.2, 920.1, 940.4, 1040.7],
            "12": [1120.1, 1070.4, 1020.3, 950.5],
            "13": [1060.2, 980.4, 940.3, 970.2],
            "14": [1000.4, 1110.1, 1040.1, 1090.5, 929.8],
            "15": [1080.8, 970.5, 1050.2, 990.2, 732.1],
            "16": [1070.2, 1030.1, 1000.7, 1050.4, 854.7]
        },
        "character_accuracies": {
            "1": [1.0, 1.0, 1.0, 1.0],
            "2": [1.0, 1.0, 0.0, 1.0],
            "3": [1.0, 0.0, 1.0, 1.0],
            "4": [1.0, 1.0, 1.0, 1.0],
            "5": [1.0, 1.0, 1.0, 1.0],
            "6": [1.0, 1.0, 0.0, 1.0],
            "7": [1.0, 1.0, 1.0, 0.0],
            "8": [1.0, 1.0, 1.0, 1.0],
            "9": [1.0, 1.0, 0.0, 1.0],
            "10": [1.0, 1.0, 1.0, 1.0],
            "11": [1.0, 1.0, 1.0, 1.0],
            "12": [1.0, 1.0, 1.0, 1.0],
            "13": [1.0, 1.0, 1.0, 1.0],
            "14": [1.0, 1.0, 1.0, 0.0],
            "15": [1.0, 1.0, 0.0, 1.0],
            "16": [1.0, 1.0, 1.0, 1.0]
        },
        "amount_correct": 13
    }
]

for results_data in results_data:
    Result.objects.create(**results_data)

update_or_create_aggregate(completed_test_3)
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


test1_response_1 = [
    {
        "response": "2456",
        "test": completed_test,
        "response_position": 1,
        "stimulus": stimulus_instance_1,
        "time_submitted": "2024-10-25T11:00:00.000Z"
    }
]
for test1_response_1 in test1_response_1:
    Response.objects.create(**test1_response_1)

test1_response_2 = [
    {
        "response": "23456",
        "test": completed_test,
        "response_position": 2,
        "stimulus": stimulus_instance_2,
        "time_submitted": "2024-10-25T11:05:00.000Z"
    }
]
for test1_response_2 in test1_response_2:
    Response.objects.create(**test1_response_2)

test1_response_3 = [
    {
        "response": "2346",
        "test": completed_test,
        "response_position": 3,
        "stimulus": stimulus_instance_3,
        "time_submitted": "2024-10-25T11:10:00.000Z"
    }
]
for test1_response_3 in test1_response_3:
    Response.objects.create(**test1_response_3)

test1_response_4 = [
    {
        "response": "1356",
        "test": completed_test,
        "response_position": 4,
        "stimulus": stimulus_instance_4,
        "time_submitted": "2024-10-25T11:15:00.000Z"
    }
]
for test1_response_4 in test1_response_4:
    Response.objects.create(**test1_response_4)

test1_response_5 = [
    {
        "response": "1245",
        "test": completed_test,
        "response_position": 5,
        "stimulus": stimulus_instance_5,
        "time_submitted": "2024-10-25T11:20:00.000Z"
    }
]
for test1_response_5 in test1_response_5:
    Response.objects.create(**test1_response_5)

test1_response_6 = [
    {
        "response": "12345",
        "test": completed_test,
        "response_position": 6,
        "stimulus": stimulus_instance_6,
        "time_submitted": "2024-10-25T11:25:00.000Z"
    }
]
for test1_response_6 in test1_response_6:
    Response.objects.create(**test1_response_6)

test1_response_7 = [
    {
        "response": "13456",
        "test": completed_test,
        "response_position": 7,
        "stimulus": stimulus_instance_7,
        "time_submitted": "2024-10-25T11:30:00.000Z"
    }
]
for test1_response_7 in test1_response_7:
    Response.objects.create(**test1_response_7)

test1_response_8 = [
    {
        "response": "12345",
        "test": completed_test,
        "response_position": 8,
        "stimulus": stimulus_instance_8,
        "time_submitted": "2024-10-25T11:35:00.000Z"
    }
]
for test1_response_8 in test1_response_8:
    Response.objects.create(**test1_response_8)

test1_response_9 = [
    {
        "response": "56KR",
        "test": completed_test,
        "response_position": 9,
        "stimulus": stimulus_instance_9,
        "time_submitted": "2024-10-25T11:40:00.000Z"
    }
]
for test1_response_9 in test1_response_9:
    Response.objects.create(**test1_response_9)

test1_response_10 = [
    {
        "response": "346LY",
        "test": completed_test,
        "response_position": 10,
        "stimulus": stimulus_instance_10,
        "time_submitted": "2024-10-25T11:45:00.000Z"
    }
]
for test1_response_10 in test1_response_10:
    Response.objects.create(**test1_response_10)

test1_response_11 = [
    {
        "response": "56FP",
        "test": completed_test,
        "response_position": 11,
        "stimulus": stimulus_instance_11,
        "time_submitted": "2024-10-25T11:50:00.000Z"
    }
]
for test1_response_11 in test1_response_11:
    Response.objects.create(**test1_response_11)

test1_response_12 = [
    {
        "response": "25RY",
        "test": completed_test,
        "response_position": 12,
        "stimulus": stimulus_instance_12,
        "time_submitted": "2024-10-25T11:55:00.000Z"
    }
]
for test1_response_12 in test1_response_12:
    Response.objects.create(**test1_response_12)

test1_response_13 = [
    {
        "response": "56LP",
        "test": completed_test,
        "response_position": 13,
        "stimulus": stimulus_instance_13,
        "time_submitted": "2024-10-25T12:00:00.000Z"
    }
]
for test1_response_13 in test1_response_13:
    Response.objects.create(**test1_response_13) 

test1_response_14 = [
    {
        "response": "134FR",
        "test": completed_test,
        "response_position": 14,
        "stimulus": stimulus_instance_14,
        "time_submitted": "2024-10-25T12:05:00.000Z"
    }
]
for test1_response_14 in test1_response_14:
    Response.objects.create(**test1_response_14)

test1_response_15 = [
    {
        "response": "136LP",
        "test": completed_test,
        "response_position": 15,
        "stimulus": stimulus_instance_15,
        "time_submitted": "2024-10-25T12:10:00.000Z"
    }
]
for test1_response_15 in test1_response_15:
    Response.objects.create(**test1_response_15)

test1_response_16 = [
    {
        "response": "246KP",
        "test": completed_test,
        "response_position": 16,
        "stimulus": stimulus_instance_16,
        "time_submitted": "2024-10-25T12:15:00.000Z"
    }
]
for test1_response_16 in test1_response_16:
    Response.objects.create(**test1_response_16)

test2_response_1 = [
    {
        "response": "654",
        "test": completed_test_2,
        "response_position": 1,
        "stimulus": stimulus_instance_1,
        "time_submitted": timezone.now() - timedelta(minutes=24)
    }
]
for test2_response_1 in test2_response_1:
    Response.objects.create(**test2_response_1)

test2_response_2 = [
    {
        "response": "46523",
        "test": completed_test_2,
        "response_position": 2,
        "stimulus": stimulus_instance_2,
        "time_submitted": timezone.now() - timedelta(minutes=23)
    }
]
for test2_response_2 in test2_response_2:
    Response.objects.create(**test2_response_2)

test2_response_3 = [
    {
        "response": "2346",
        "test": completed_test_2,
        "response_position": 3,
        "stimulus": stimulus_instance_3,
        "time_submitted": timezone.now() - timedelta(minutes=22)
    }
]
for test2_response_3 in test2_response_3:
    Response.objects.create(**test2_response_3)

test2_response_4 = [
    {
        "response": "1356",
        "test": completed_test_2,
        "response_position": 4,
        "stimulus": stimulus_instance_4,
        "time_submitted": timezone.now() - timedelta(minutes=21)
    }
]

test2_response_5 = [
    {
        "response": "1245",
        "test": completed_test_2,
        "response_position": 5,
        "stimulus": stimulus_instance_5,
        "time_submitted": timezone.now() - timedelta(minutes=21)
    }
]
for test2_response_5 in test2_response_5:    
    Response.objects.create(**test2_response_5)

test2_response_6 = [
    {
        "response": "12345",
        "test": completed_test_2,
        "response_position": 6,
        "stimulus": stimulus_instance_6,
        "time_submitted": timezone.now() - timedelta(minutes=21)
    }
]
for test2_response_6 in test2_response_6:
    Response.objects.create(**test2_response_6)

test2_response_7 = [
    {
        "response": "13456",
        "test": completed_test_2,
        "response_position": 7,
        "stimulus": stimulus_instance_7,
        "time_submitted": timezone.now() - timedelta(minutes=21)
    }
]
for test2_response_7 in test2_response_7:
    Response.objects.create(**test2_response_7)

test2_response_8 = [
    {
        "response": "12345",
        "test": completed_test_2,
        "response_position": 8,
        "stimulus": stimulus_instance_8,
        "time_submitted": timezone.now() - timedelta(minutes=20)
    }
]
for test2_response_8 in test2_response_8:
    Response.objects.create(**test2_response_8)

test2_response_9 = [
    {
        "response": "5KR6",
        "test": completed_test_2,
        "response_position": 9,
        "stimulus": stimulus_instance_9,
        "time_submitted": timezone.now() - timedelta(minutes=16)
    }
]
for test2_response_9 in test2_response_9:
    Response.objects.create(**test2_response_9)

test2_response_10 = [
    {
        "response": "346KY",
        "test": completed_test_2,
        "response_position": 10,
        "stimulus": stimulus_instance_10,
        "time_submitted": timezone.now() - timedelta(minutes=16)
    }
]
for test2_response_10 in test2_response_10:
    Response.objects.create(**test2_response_10)

test2_response_11 = [
    {
        "response": "56FP",
        "test": completed_test_2,
        "response_position": 11,
        "stimulus": stimulus_instance_11,
        "time_submitted": timezone.now() - timedelta(minutes=16)
    }
]
for test2_response_11 in test2_response_11:
    Response.objects.create(**test2_response_11)

test2_response_12 = [
    {
        "response": "25RY",
        "test": completed_test_2,
        "response_position": 12,
        "stimulus": stimulus_instance_12,
        "time_submitted": timezone.now() - timedelta(minutes=16)
    }
]
for test2_response_12 in test2_response_12:
    Response.objects.create(**test2_response_12)

test2_response_13 = [
    {
        "response": "56LP",
        "test": completed_test_2,
        "response_position": 13,
        "stimulus": stimulus_instance_13,
        "time_submitted": timezone.now() - timedelta(minutes=14)
    }
]
for test2_response_13 in test2_response_13:
    Response.objects.create(**test2_response_13)

test2_response_14 = [
    {
        "response": "134RY",
        "test": completed_test_2,
        "response_position": 14,
        "stimulus": stimulus_instance_14,
        "time_submitted": timezone.now() - timedelta(minutes=14)
    }
]
for test2_response_14 in test2_response_14:
    Response.objects.create(**test2_response_14)

test2_response_15 = [
    {
        "response": "136RY",
        "test": completed_test_2,
        "response_position": 15,
        "stimulus": stimulus_instance_15,
        "time_submitted": timezone.now() - timedelta(minutes=13)
    }
]
for test2_response_15 in test2_response_15:
    Response.objects.create(**test2_response_15)

test2_response_16 = [
    {
        "response": "246PR",
        "test": completed_test_2,
        "response_position": 16,
        "stimulus": stimulus_instance_16,
        "time_submitted": timezone.now() - timedelta(minutes=13)
    }
]
for test2_response_16 in test2_response_16:
    Response.objects.create(**test2_response_16)

test3_response_1 = [
    {
        "response": "2456",
        "test": completed_test_3,
        "response_position": 1,
        "stimulus": stimulus_instance_1,
        "time_submitted": timezone.now() - timedelta(minutes=45),
    }
]
for test3_response_1 in test3_response_1:
    Response.objects.create(**test3_response_1)

test3_response_2 = [
    {
        "response": "23416",
        "test": completed_test_3,
        "response_position": 2,
        "stimulus": stimulus_instance_2,
        "time_submitted": timezone.now() - timedelta(minutes=45),
    }
]
for test3_response_2 in test3_response_2:
    Response.objects.create(**test3_response_2)

test3_response_3 = [
    {
        "response": "2356",
        "test": completed_test_3,
        "response_position": 3,
        "stimulus": stimulus_instance_3,
        "time_submitted": timezone.now() - timedelta(minutes=44),
    }
]
for test3_response_3 in test3_response_3:
    Response.objects.create(**test3_response_3)

test3_response_4 = [
    {
        "response": "1356",
        "test": completed_test_3,
        "response_position": 4,
        "stimulus": stimulus_instance_4,
        "time_submitted": timezone.now() - timedelta(minutes=44),
    }
]
for test3_response_4 in test3_response_4:
    Response.objects.create(**test3_response_4)

test3_response_5 = [
    {
        "response": "1245",
        "test": completed_test_3,
        "response_position": 5,
        "stimulus": stimulus_instance_5,
        "time_submitted": timezone.now() - timedelta(minutes=44),
    }
]
for test3_response_5 in test3_response_5:
    Response.objects.create(**test3_response_5)

test3_response_6 = [
    {
        "response": "11346",
        "test": completed_test_3,
        "response_position": 6,
        "stimulus": stimulus_instance_6,
        "time_submitted": timezone.now() - timedelta(minutes=43),
    }
]
for test3_response_6 in test3_response_6:
    Response.objects.create(**test3_response_6)

test3_response_7 = [
    {
        "response": "13456",
        "test": completed_test_3,
        "response_position": 7,
        "stimulus": stimulus_instance_7,
        "time_submitted": timezone.now() - timedelta(minutes=43),
    }
]
for test3_response_7 in test3_response_7:
    Response.objects.create(**test3_response_7)

test3_response_8 = [
    {
        "response": "12346",
        "test": completed_test_3,
        "response_position": 8,
        "stimulus": stimulus_instance_8,
        "time_submitted": timezone.now() - timedelta(minutes=43),
    }
]
for test3_response_8 in test3_response_8:
    Response.objects.create(**test3_response_8)

test3_response_9 = [
    {
        "response": "54KR",
        "test": completed_test_3,
        "response_position": 9,
        "stimulus": stimulus_instance_9,
        "time_submitted": timezone.now() - timedelta(minutes=41),
    }
]
for test3_response_9 in test3_response_9:
    Response.objects.create(**test3_response_9)

test3_response_10 = [
    {
        "response": "346KP",
        "test": completed_test_3,
        "response_position": 10,
        "stimulus": stimulus_instance_10,
        "time_submitted": timezone.now() - timedelta(minutes=40),
    }
]
for test3_response_10 in test3_response_10:
    Response.objects.create(**test3_response_10)

test3_response_11 = [
    {
        "response": "56FP",
        "test": completed_test_3,
        "response_position": 11,
        "stimulus": stimulus_instance_11,
        "time_submitted": timezone.now() - timedelta(minutes=39),
    }
]
for test3_response_11 in test3_response_11:
    Response.objects.create(**test3_response_11)

test3_response_12 = [
    {
        "response": "25RY",
        "test": completed_test_3,
        "response_position": 12,
        "stimulus": stimulus_instance_12,
        "time_submitted": timezone.now() - timedelta(minutes=39),
    }
]
for test3_response_12 in test3_response_12:
    Response.objects.create(**test3_response_12)

test3_response_13 = [
    {
        "response": "56LP",
        "test": completed_test_3,
        "response_position": 13,
        "stimulus": stimulus_instance_13,
        "time_submitted": timezone.now() - timedelta(minutes=38),
    }
]
for test3_response_13 in test3_response_13:
    Response.objects.create(**test3_response_13)

test3_response_14 = [
    {
        "response": "134RY",
        "test": completed_test_3,
        "response_position": 14,
        "stimulus": stimulus_instance_14,
        "time_submitted": timezone.now() - timedelta(minutes=37),
    }
]
for test3_response_14 in test3_response_14:
    Response.objects.create(**test3_response_14)

test3_response_15 = [
    {
        "response": "136LY",
        "test": completed_test_3,
        "response_position": 15,
        "stimulus": stimulus_instance_15,
        "time_submitted": timezone.now() - timedelta(minutes=37),
    }
]
for test3_response_15 in test3_response_15:
    Response.objects.create(**test3_response_15)

test3_response_16 = [
    {
        "response": "246KP",
        "test": completed_test_3,
        "response_position": 16,
        "stimulus": stimulus_instance_16,
        "time_submitted": timezone.now() - timedelta(minutes=37),
    }
]
for test3_response_16 in test3_response_16:
    Response.objects.create(**test3_response_16)

# Enter more test responses below...

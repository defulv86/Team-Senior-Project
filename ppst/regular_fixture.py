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

# Create another user as medical personnel: 'DoctorWho' with password '@password115'
doctor_who = User.objects.create_user(username='DoctorWho', password='@password115', email='doctorwho@example.com', first_name='Doctor', last_name='Who')

# Create additional doctors as medical personnel
mitchell_A = User.objects.create_user(username='Mitchell_A', password='935abc115!', email='mitchell@example.com', first_name='Mitchell', last_name='Anderson')

clark_H = User.objects.create_user(username='Clark_H', password='healthy!mind2024', email='clark@example.com', first_name='Clark', last_name='Hawkins')

alexandria_P = User.objects.create_user(username='Becky_P', password='@tree_frog123', email='becky@example.com', first_name='Becky', last_name='Parker')

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
	age=29,
	created_at=timezone.now() - timedelta(minutes=45),
	started_at=timezone.now() - timedelta(minutes=40),
	finished_at=timezone.now() - timedelta(minutes=30),
	status='completed'
)

completed_test_5 = Test.objects.create(
    user=doctor_who,
    age=30,
    created_at=timezone.now() - timedelta(days=5, hours=23, minutes=59),
    started_at=timezone.now() - timedelta(days=5, hours=23, minutes=58),
    finished_at=timezone.now() - timedelta(days=5, hours=23, minutes=57),
    status='completed'
)

completed_test_6 = Test.objects.create(
    user=mitchell_A,
    age=51,
    created_at=timezone.now() - timedelta(days=15, hours=23, minutes=59),
    started_at=timezone.now() - timedelta(days=14, hours=3, minutes=22),
    finished_at=timezone.now() - timedelta(days=14, hours=3, minutes=12, seconds=58),
    status='completed'
)

completed_test_7 = Test.objects.create(
    user=clark_H,
    age=53,
    created_at="2024-11-17T11:33:00Z",
    started_at="2024-11-17T19:12:00Z", 
    finished_at="2024-11-17T19:17:02Z",
    status='completed'
)

completed_test_8 = Test.objects.create(
    user=alexandria_P,
    age=55,
    created_at="2024-11-17T13:43:00Z",
    started_at="2024-11-17T19:27:00Z",
    finished_at="2024-11-17T19:30:30Z",
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
            "1": [2558.2, 941.9, 1351.8, 1117.7],
            "2": [7305.4, 0.0, 0.0, 0.0, 0.0],
            "3": [4053.5, 3857.1, 1762.7, 808.7],
            "4": [2345.6, 2437.0, 1067.6, 1224.3],
            "5": [1437.4, 1231.4, 2569.5, 737.4],
            "6": [1752.8, 886.7, 537.0, 757.7, 1793.9],
            "7": [3834.1, 944.0, 1103.5, 860.1, 939.8],
            "8": [1315.1, 1162.1, 1012.6, 746.1, 723.6],
            "9": [4362.2, 1507.7, 2262.1, 887.9],
            "10": [22097.1, 981.6, 1055.5, 985.9, 1230.7],
            "11": [6894.4, 1259.5, 1911.6, 2181.2],
            "12": [3670.4, 1223.7, 2883.5, 1465.2],
            "13": [6108.3, 1315.2, 1779.2, 978.9],
            "14": [5660, 2138.8, 1308.0, 4587.2, 766.5],
            "15": [7557.9, 1098.1, 1326.3, 647.9, 0.0],
            "16": [5090.6, 949.2, 5895.1, 3031.5, 2412.1]
            },
        "character_accuracies": {
            "1": [0.0, 0.0, 1.0, 0.0],
            "2": [1.0, 0.0, 0.0, 0.0, 0.0],
            "3": [1.0, 1.0, 1.0, 1.0],
            "4": [1.0, 1.0, 1.0, 1.0],
            "5": [1.0, 1.0, 1.0, 1.0],
            "6": [1.0, 1.0, 0.0, 0.0, 0.0],
            "7": [1.0, 0.0, 0.0, 0.0, 0.0],
            "8": [1.0, 1.0, 1.0, 1.0, 1.0],
            "9": [1.0, 1.0, 1.0, 1.0],
            "10": [0.0, 0.0, 0.0, 0.0, 0.0],
            "11": [1.0, 1.0, 1.0, 1.0],
            "12": [1.0, 1.0, 1.0, 1.0],
            "13": [1.0, 1.0, 1.0, 1.0],
            "14": [1.0, 1.0, 1.0, 1.0, 1.0],
            "15": [0.0, 0.0, 0.0, 0.0, 0.0],
            "16": [1.0, 1.0, 1.0, 1.0, 1.0]
        },
        "amount_correct": 10
    },
    {
        "test": completed_test_5,
        "character_latencies": {
            "1": [3071.7, 1015.4, 2135.2, 2181.0],
            "2": [2118.4, 2547.8, 1784.6, 1809.6, 2138.2],
            "3": [1434.0, 1743.1, 1097.5, 1191.7],
            "4": [1693.3, 1444.0, 1265.3, 1660.8],
            "5": [1737.1, 1731.1, 1300.8, 2068.4],
            "6": [1515.9, 1323.3, 1849.7, 1710.3, 1278.7],
            "7": [1598.4, 1262.7, 1580.2, 1861.8, 1596.5],
            "8": [1510.8, 1337.4, 1900.1, 1377.7, 0.0],
            "9": [5726.9, 1398.9, 1253.1, 2237.7],
            "10": [3375.7, 1943.5, 1889.7, 1856.9, 1020.6],
            "11": [3287.4, 1761.9, 2193.2, 1385.3],
            "12": [3848.6, 2172.5, 1814.8, 1739.0],
            "13": [6357.7, 2117.7, 1549.8, 1024.0],
            "14": [2938.6, 1317.0, 3438.4, 4503.8, 1223.8],
            "15": [1919.7, 1259.7, 1647.7, 1884.9, 921.8],
            "16": [4207.5, 1028.1, 1126.4, 2965.4, 1816.2]
        },
        "character_accuracies": {
            "1": [1.0, 1.0, 1.0, 1.0],
            "2": [1.0, 1.0, 1.0, 1.0, 1.0],
            "3": [1.0, 1.0, 1.0, 1.0],
            "4": [1.0, 1.0, 1.0, 1.0],
            "5": [1.0, 1.0, 1.0, 1.0],
            "6": [1.0, 1.0, 1.0, 1.0, 1.0],
            "7": [1.0, 1.0, 1.0, 1.0, 1.0],
            "8": [1.0, 0.0, 0.0, 0.0, 0.0],
            "9": [1.0, 1.0, 1.0, 1.0],
            "10": [1.0, 1.0, 1.0, 1.0, 1.0],
            "11": [1.0, 1.0, 1.0, 1.0],
            "12": [1.0, 1.0, 1.0, 1.0],
            "13": [1.0, 0.0, 0.0, 0.0],
            "14": [1.0, 1.0, 1.0, 1.0, 1.0],
            "15": [1.0, 1.0, 1.0, 1.0, 1.0],
            "16": [1.0, 1.0, 1.0, 1.0, 1.0]
        },
        "amount_correct": 14
    },
    {
        "test": completed_test_6,
        "character_latencies": {
            "1": [3244.2, 1544.8, 1706.0, 1636.9],
            "2": [2478.2, 1376.9, 2096.6, 1599.3, 1933.3],
            "3": [14149.3, 1384.2, 1459.5, 1242.8],
            "4": [5654.6, 1559.7, 1337.4, 1507.6],
            "5": [6157.0, 1619.4, 1291.5, 1507.6],
            "6": [7813.9, 5891.4, 7069.4, 1638.1, 1355.1],
            "7": [4482.5, 10679.1, 4115.6, 1402.5, 1495.5],
            "8": [2550.3, 1588.8, 1634.1, 2046.0, 1470.7],
            "9": [7227.5, 2160.4, 2134.0, 1342.0],
            "10": [12243.6, 14729.5, 9414, 1547.6, 1615.8],
            "11": [5279.7, 1698.7, 1708.2, 1214.1],
            "12": [4967.0, 1711.9, 2043.8, 1462.4],
            "13": [3719.7, 1761.9, 2043.8, 1544.0],
            "14": [8508.8, 1914.2, 1556.5, 2026.8, 1370.4],
            "15": [1982.2, 1391.1, 1555.0, 2519.6, 1418.1],
            "16": [3787.5, 1418.7, 1495.9, 8046.7, 1244.7]
        },
        "character_accuracies": {
            "1": [0.0, 0.0, 1.0, 0.0],
            "2": [0.0, 0.0, 0.0, 0.0, 0.0],
            "3": [1.0, 1.0, 1.0, 1.0],
            "4": [1.0, 1.0, 1.0, 1.0],
            "5": [1.0, 1.0, 1.0, 1.0],
            "6": [1.0, 1.0, 1.0, 1.0, 1.0],
            "7": [1.0, 1.0, 1.0, 1.0, 1.0],
            "8": [1.0, 1.0, 1.0, 1.0, 1.0],
            "9": [1.0, 1.0, 1.0, 1.0],
            "10": [0.0, 1.0, 0.0, 1.0, 1.0],
            "11": [1.0, 1.0, 1.0, 1.0],
            "12": [1.0, 1.0, 1.0, 1.0],
            "13": [1.0, 1.0, 1.0, 1.0],
            "14": [1.0, 1.0, 1.0, 1.0, 1.0],
            "15": [1.0, 1.0, 1.0, 1.0, 1.0],
            "16": [1.0, 1.0, 1.0, 0.0, 0.0]
        },
        "amount_correct": 12
    },
    {
        "test": completed_test_7,
        "character_latencies": {
            "1": [2221.4, 586.1, 7899.0],
            "2": [4392.4, 943.9, 767.7, 2816.9, 569.1],
            "3": [2390.8, 1203.1, 1078.3, 690.8],
            "4": [1361.6, 1087.7, 3572.6, 947.9],
            "5": [4317.5, 3524.3, 1162.2, 901.4],
            "6": [2635.8, 587.1, 802.4, 3192.0, 530.6],
            "7": [4454.9, 1536.2, 4042.8, 4962.1],
            "8": [1495.4, 1007.5, 3944.8, 1520.5, 612.5],
            "9": [2702.1, 1115.7, 4134.0, 510.7],
            "10": [6120.9, 712.7, 667.4, 2126.1, 474.4],
            "11": [3514.3, 1173.0, 1778.1, 588.3],
            "12": [2929.0, 1401.1, 3980.8, 696.5],
            "13": [3333.8, 816.3, 3627.5, 591.5],
            "14": [1336.5, 1819.7, 1195.3, 965.3, 1076.6],
            "15": [4608.8, 791.4, 1570.3, 3598.6, 770.6],
            "16": [6797.2, 460.3, 473.5, 5438.7, 671.0]
        },
        "character_accuracies": {
            "1": [1.0, 1.0, 0.0, 0.0],
            "2": [1.0, 1.0, 1.0, 1.0, 1.0],
            "3": [1.0, 1.0, 1.0, 1.0],
            "4": [1.0, 1.0, 1.0, 1.0],
            "5": [1.0, 1.0, 1.0, 1.0],
            "6": [1.0, 1.0, 1.0, 1.0, 1.0],
            "7": [1.0, 1.0, 1.0, 0.0, 0.0],
            "8": [1.0, 1.0, 1.0, 1.0, 1.0],
            "9": [1.0, 1.0, 1.0, 1.0],
            "10": [1.0, 1.0, 1.0, 1.0, 1.0],
            "11": [1.0, 1.0, 1.0, 1.0],
            "12": [1.0, 1.0, 1.0, 1.0],
            "13": [1.0, 1.0, 1.0, 1.0],
            "14": [1.0, 1.0, 1.0, 1.0, 1.0],
            "15": [1.0, 1.0, 1.0, 0.0, 1.0],
            "16": [1.0, 1.0, 1.0, 1.0, 1.0]
        },
        "amount_correct": 13
    },
    {
        "test": completed_test_8,
        "character_latencies": {
            "1": [1219.8, 786.1, 841.4, 902.6],
            "2": [1033.5, 936.1, 860.5, 819.5, 868.7],
            "3": [1203.2, 982.8, 1472.5, 821.4],
            "4": [873.0, 853.5, 1133.5, 731.3],
            "5": [1105.6, 798.7, 793.8, 736.9],
            "6": [1092.3, 896.6, 758.8, 939.1, 744.7],
            "7": [1589.7, 915.1, 764.2, 783.7, 762.4],
            "8": [983.8, 934.3, 918.4, 1114.7, 825.2],
            "9": [2147.4, 901.6, 757.1, 618.5],
            "10": [3444.4, 879.7, 779.4, 1509.9, 617.3],
            "11": [1165.9, 1033.6, 1191.9, 559.1],
            "12": [1212.9, 885.7, 1986.2, 890.0],
            "13": [1583.7, 1061.9, 1213.9, 853.8],
            "14": [1726.0, 804.8, 902.5, 1153.1, 4439.4],
            "15": [1362.7, 763.0, 2159.8, 970.6, 703.1],
            "16": [1490.1, 716.9, 855.9, 770.5, 833.3]
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
            "14": [1.0, 1.0, 1.0, 1.0, 0.0],
            "15": [1.0, 1.0, 1.0, 1.0, 1.0],
            "16": [1.0, 1.0, 1.0, 1.0, 1.0]
        },
        "amount_correct": 15
    }
    # Add more tests results if needed (Only real data.)
]

for results_data in results_data:
	Result.objects.create(**results_data)

update_or_create_aggregate(completed_test)
update_or_create_aggregate(completed_test_2)
update_or_create_aggregate(completed_test_3)
update_or_create_aggregate(completed_test_4)
update_or_create_aggregate(completed_test_5)
update_or_create_aggregate(completed_test_6)
update_or_create_aggregate(completed_test_7)
update_or_create_aggregate(completed_test_8)

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
for test2_response_4 in test2_response_4:
	Response.objects.create(**test2_response_4)


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

test4_response_1 = [
    {
        "response": "6254",
        "test": completed_test_4,
        "response_position": 1,
        "stimulus": stimulus_instance_1,
        "time_submitted": "2024-11-28T21:45:00.000Z"
    }
]
for test4_response_1 in test4_response_1:
    Response.objects.create(**test4_response_1)

test4_response_2 = [
    {
        "response": "2",
        "test": completed_test_4,
        "response_position": 2,
        "stimulus": stimulus_instance_2,
        "time_submitted": "2024-11-28T21:45:00.000Z"
    }
]
for test4_response_2 in test4_response_2:
    Response.objects.create(**test4_response_2)

test4_response_3 = [
    {
        "response": "2346",
        "test": completed_test_4,
        "response_position": 3,
        "stimulus": stimulus_instance_3,
        "time_submitted": "2024-11-28T21:46:00.000Z"
    }
]
for test4_response_3 in test4_response_3:
    Response.objects.create(**test4_response_3)

test4_response_4 = [
    {
        "response": "1356",
        "test": completed_test_4,
        "response_position": 4,
        "stimulus": stimulus_instance_4,
        "time_submitted": "2024-11-28T21:46:00.000Z"
    }
]
for test4_response_4 in test4_response_4:
    Response.objects.create(**test4_response_4)

test4_response_5 = [
    {
        "response": "1245",
        "test": completed_test_4,
        "response_position": 5,
        "stimulus": stimulus_instance_5,
        "time_submitted": "2024-11-28T21:46:00.000Z"
    }
]
for test4_response_5 in test4_response_5:
    Response.objects.create(**test4_response_5)

test4_response_6 = [
    {
        "response": "12456",
        "test": completed_test_4,
        "response_position": 6,
        "stimulus": stimulus_instance_6,
        "time_submitted": "2024-11-28T21:46:00.000Z"
    }
]
for test4_response_6 in test4_response_6:
    Response.objects.create(**test4_response_6)

test4_response_7 = [
    {
        "response": "12345",
        "test": completed_test_4,
        "response_position": 7,
        "stimulus": stimulus_instance_7,
        "time_submitted": "2024-11-28T21:47:00.000Z"
    }
]
for test4_response_7 in test4_response_7:
    Response.objects.create(**test4_response_7)

test4_response_8 = [
    {
        "response": "12345",
        "test": completed_test_4,
        "response_position": 8,
        "stimulus": stimulus_instance_8,
        "time_submitted": "2024-11-28T21:47:00.000Z"
    }
]
for test4_response_8 in test4_response_8:
    Response.objects.create(**test4_response_8)

test4_response_9 = [
    {
        "response": "56KR",
        "test": completed_test_4,
        "response_position": 9,
        "stimulus": stimulus_instance_9,
        "time_submitted": "2024-11-28T21:49:00.000Z"
    }
]
for test4_response_9 in test4_response_9:
    Response.objects.create(**test4_response_9)

test4_response_10 = [
    {
        "response": "152PK",
        "test": completed_test_4,
        "response_position": 10,
        "stimulus": stimulus_instance_10,
        "time_submitted": "2024-11-28T21:50:00.000Z"
    }
]
for test4_response_10 in test4_response_10:
    Response.objects.create(**test4_response_10)

test4_response_11 = [
    {
        "response": "56FP",
        "test": completed_test_4,
        "response_position": 11,
        "stimulus": stimulus_instance_11,
        "time_submitted": "2024-11-28T21:50:00.000Z"
    }
]
for test4_response_11 in test4_response_11:
    Response.objects.create(**test4_response_11)

test4_response_12 = [
    {
        "response": "25RY",
        "test": completed_test_4,
        "response_position": 12,
        "stimulus": stimulus_instance_12,
        "time_submitted": "2024-11-28T21:50:00.000Z"
    }
]
for test4_response_12 in test4_response_12:
    Response.objects.create(**test4_response_12)

test4_response_13 = [
    {
        "response": "56LP",
        "test": completed_test_4,
        "response_position": 13,
        "stimulus": stimulus_instance_13,
        "time_submitted": "2024-11-28T21:51:00.000Z"
    }
]
for test4_response_13 in test4_response_13:
    Response.objects.create(**test4_response_13)

test4_response_14 = [
    {
        "response": "134FR",
        "test": completed_test_4,
        "response_position": 14,
        "stimulus": stimulus_instance_14,
        "time_submitted": "2024-11-28T21:51:00.000Z"
    }
]
for test4_response_14 in test4_response_14:
    Response.objects.create(**test4_response_14)

test4_response_15 = [
    {
        "response": "36LY",
        "test": completed_test_4,
        "response_position": 15,
        "stimulus": stimulus_instance_15,
        "time_submitted": "2024-11-28T21:51:00.000Z"
    }
]
for test4_response_15 in test4_response_15:
    Response.objects.create(**test4_response_15)

test4_response_16 = [
    {
        "response": "246KP",
        "test": completed_test_4,
        "response_position": 16,
        "stimulus": stimulus_instance_16,
        "time_submitted": "2024-11-28T21:52:00.000Z"
    }
]
for test4_response_16 in test4_response_16:
    Response.objects.create(**test4_response_16)

test5_response_1 = [
    {
        "response": "2456",
        "test": completed_test_5,
        "response_position": 1,
        "stimulus": stimulus_instance_1,
        "time_submitted": "2024-11-28T21:58:00.000Z"
    }
]
for test5_response_1 in test5_response_1:
    Response.objects.create(**test5_response_1)

test5_response_2 = [
    {
        "response": "23456",
        "test": completed_test_5,
        "response_position": 2,
        "stimulus": stimulus_instance_2,
        "time_submitted": "2024-11-28T21:59:00.000Z"
    }
]
for test5_response_2 in test5_response_2:
    Response.objects.create(**test5_response_2)

test5_response_3 = [
    {
        "response": "2346",
        "test": completed_test_5,
        "response_position": 3,
        "stimulus": stimulus_instance_3,
        "time_submitted": "2024-11-28T21:59:00.000Z"
    }
]
for test5_response_3 in test5_response_3:
    Response.objects.create(**test5_response_3)

test5_response_4 = [
    {
        "response": "1356",
        "test": completed_test_5,
        "response_position": 4,
        "stimulus": stimulus_instance_4,
        "time_submitted": "2024-11-28T21:59:00.000Z"
    }
]
for test5_response_4 in test5_response_4:
    Response.objects.create(**test5_response_4)

test5_response_5 = [
    {
        "response": "1245",
        "test": completed_test_5,
        "response_position": 5,
        "stimulus": stimulus_instance_5,
        "time_submitted": "2024-11-28T22:00:00.000Z"
    }
]
for test5_response_5 in test5_response_5:
    Response.objects.create(**test5_response_5)

test5_response_6 = [
    {
        "response": "12345",
        "test": completed_test_5,
        "response_position": 6,
        "stimulus": stimulus_instance_6,
        "time_submitted": "2024-11-28T22:00:00.000Z"
    }
]
for test5_response_6 in test5_response_6:
    Response.objects.create(**test5_response_6)

test5_response_7 = [
    {
        "response": "13456",
        "test": completed_test_5,
        "response_position": 7,
        "stimulus": stimulus_instance_7,
        "time_submitted": "2024-11-28T22:00:00.000Z"
    }
]
for test5_response_7 in test5_response_7:
    Response.objects.create(**test5_response_7)

test5_response_8 = [
    {
        "response": "1345",
        "test": completed_test_5,
        "response_position": 8,
        "stimulus": stimulus_instance_8,
        "time_submitted": "2024-11-28T22:00:00.000Z"
    }
]
for test5_response_8 in test5_response_8:
    Response.objects.create(**test5_response_8)

test5_response_9 = [
    {
        "response": "56KR",
        "test": completed_test_5,
        "response_position": 9,
        "stimulus": stimulus_instance_9,
        "time_submitted": "2024-11-28T22:01:00.000Z"
    }
]
for test5_response_9 in test5_response_9:
    Response.objects.create(**test5_response_9)

test5_response_10 = [
    {
        "response": "346LY",
        "test": completed_test_5,
        "response_position": 10,
        "stimulus": stimulus_instance_10,
        "time_submitted": "2024-11-28T22:01:00.000Z"
    }
]
for test5_response_10 in test5_response_10:
    Response.objects.create(**test5_response_10)

test5_response_11 = [
    {
        "response": "56FP",
        "test": completed_test_5,
        "response_position": 11,
        "stimulus": stimulus_instance_11,
        "time_submitted": "2024-11-28T22:02:00.000Z"
    }
]
for test5_response_11 in test5_response_11:
    Response.objects.create(**test5_response_11)

test5_response_12 = [
    {
        "response": "25RY",
        "test": completed_test_5,
        "response_position": 12,
        "stimulus": stimulus_instance_12,
        "time_submitted": "2024-11-28T22:02:00.000Z"
    }
]
for test5_response_12 in test5_response_12:
    Response.objects.create(**test5_response_12)

test5_response_13 = [
    {
        "response": "5LPY",
        "test": completed_test_5,
        "response_position": 13,
        "stimulus": stimulus_instance_13,
        "time_submitted": "2024-11-28T22:03:00.000Z"
    }
]
for test5_response_13 in test5_response_13:
    Response.objects.create(**test5_response_13)

test5_response_14 = [
    {
        "response": "134FR",
        "test": completed_test_5,
        "response_position": 14,
        "stimulus": stimulus_instance_14,
        "time_submitted": "2024-11-28T22:03:00.000Z"
    }
]
for test5_response_14 in test5_response_14:
    Response.objects.create(**test5_response_14)

test5_response_15 = [
    {
        "response": "136LY",
        "test": completed_test_5,
        "response_position": 15,
        "stimulus": stimulus_instance_15,
        "time_submitted": "2024-11-28T22:03:00.000Z"
    }
]
for test5_response_15 in test5_response_15:
    Response.objects.create(**test5_response_15)

test5_response_16 = [
    {
        "response": "246KP",
        "test": completed_test_5,
        "response_position": 16,
        "stimulus": stimulus_instance_16,
        "time_submitted": "2024-11-28T22:04:00.000Z"
    }
]
for test5_response_16 in test5_response_16:
    Response.objects.create(**test5_response_16)

test6_response_1 = [
    {
        "response": "6254",
        "test": completed_test_6,
        "response_position": 1,
        "stimulus": stimulus_instance_1,
        "time_submitted": "2024-12-04T18:39:04Z"
    }
]
for test6_response_1 in test6_response_1:
    Response.objects.create(**test6_response_1)

test6_response_2 = [
    {
        "response": "46523",
        "test": completed_test_6,
        "response_position": 2,
        "stimulus": stimulus_instance_2,
        "time_submitted": "2024-12-04T18:39:24Z"
    }
]
for test6_response_2 in test6_response_2:
    Response.objects.create(**test6_response_2)

test6_response_3 = [
    {
        "response": "2346",
        "test": completed_test_6,
        "response_position": 3,
        "stimulus": stimulus_instance_3,
        "time_submitted": "2024-12-04T18:40:48Z"
    }
]
for test6_response_3 in test6_response_3:
    Response.objects.create(**test6_response_3)

test6_response_4 = [
    {
        "response": "1356",
        "test": completed_test_6,
        "response_position": 4,
        "stimulus": stimulus_instance_4,
        "time_submitted": "2024-12-04T18:41:06Z"
    }
]
for test6_response_4 in test6_response_4:
    Response.objects.create(**test6_response_4)

test6_response_5 = [
    {
        "response": "1245",
        "test": completed_test_6,
        "response_position": 5,
        "stimulus": stimulus_instance_5,
        "time_submitted": "2024-12-04T18:41:27Z"
    }
]
for test6_response_5 in test6_response_5:
    Response.objects.create(**test6_response_5)

test6_response_6 = [
    {
        "response": "12345",
        "test": completed_test_6,
        "response_position": 6,
        "stimulus": stimulus_instance_6,
        "time_submitted": "2024-12-04T18:42:01Z"
    }
]
for test6_response_6 in test6_response_6:
    Response.objects.create(**test6_response_6)

test6_response_7 = [
    {
        "response": "13456",
        "test": completed_test_6,
        "response_position": 7,
        "stimulus": stimulus_instance_7,
        "time_submitted": "2024-12-04T18:42:32Z"
    }
]
for test6_response_7 in test6_response_7:
    Response.objects.create(**test6_response_7)

test6_response_8 = [
    {
        "response": "12345",
        "test": completed_test_6,
        "response_position": 8,
        "stimulus": stimulus_instance_8,
        "time_submitted": "2024-12-04T18:42:52Z"
    }
]
for test6_response_8 in test6_response_8:
    Response.objects.create(**test6_response_8)

test6_response_9 = [
    {
        "response": "6R5K",
        "test": completed_test_6,
        "response_position": 9,
        "stimulus": stimulus_instance_9,
        "time_submitted": "2024-12-04T18:44:05Z"
    }
]
for test6_response_9 in test6_response_9:
    Response.objects.create(**test6_response_9)

test6_response_10 = [
    {
        "response": "64KLY",
        "test": completed_test_6,
        "response_position": 10,
        "stimulus": stimulus_instance_10,
        "time_submitted": "2024-12-04T18:44:54Z"
    }
]
for test6_response_10 in test6_response_10:
    Response.objects.create(**test6_response_10)

test6_response_11 = [
    {
        "response": "56FP",
        "test": completed_test_6,
        "response_position": 11,
        "stimulus": stimulus_instance_11,
        "time_submitted": "2024-12-04T18:45:23Z"
    }
]
for test6_response_11 in test6_response_11:
    Response.objects.create(**test6_response_11)

test6_response_12 = [
    {
        "response": "25RY",
        "test": completed_test_6,
        "response_position": 12,
        "stimulus": stimulus_instance_12,
        "time_submitted": "2024-12-04T18:45:42Z"
    }
]
for test6_response_12 in test6_response_12:
    Response.objects.create(**test6_response_12)

test6_response_13 = [
    {
        "response": "56LP",
        "test": completed_test_6,
        "response_position": 13,
        "stimulus": stimulus_instance_13,
        "time_submitted": "2024-12-04T18:45:59Z"
    }
]
for test6_response_13 in test6_response_13:
    Response.objects.create(**test6_response_13)

test6_response_14 = [
    {
        "response": "134FR",
        "test": completed_test_6,
        "response_position": 14,
        "stimulus": stimulus_instance_14,
        "time_submitted": "2024-12-04T18:46:24Z"
    }
]
for test6_response_14 in test6_response_14:
    Response.objects.create(**test6_response_14)

test6_response_15 = [
    {
        "response": "136LY",
        "test": completed_test_6,
        "response_position": 15,
        "stimulus": stimulus_instance_15,
        "time_submitted": "2024-12-04T18:46:42Z"
    }
]
for test6_response_15 in test6_response_15:
    Response.objects.create(**test6_response_15)

test6_response_16 = [
    {
        "response": "246PR",
        "test": completed_test_6,
        "response_position": 16,
        "stimulus": stimulus_instance_16,
        "time_submitted": "2024-12-04T18:47:07Z"
    }
]
for test6_response_16 in test6_response_16:
    Response.objects.create(**test6_response_16)

test7_response_1 = [
    {
        "response": "246",
        "test": completed_test_7,
        "response_position": 1,
        "stimulus": stimulus_instance_1,
        "time_submitted": "2024-11-17T19:12:00.000Z"
    }
]
for test7_response_1 in test7_response_1:
    Response.objects.create(**test7_response_1)

test7_response_2 = [
    {
        "response": "23456",
        "test": completed_test_7,
        "response_position": 2,
        "stimulus": stimulus_instance_2,
        "time_submitted": "2024-11-17T19:12:00.000Z"
    }
]
for test7_response_2 in test7_response_2:
    Response.objects.create(**test7_response_2)

test7_response_3 = [
    {
        "response": "2346",
        "test": completed_test_7,
        "response_position": 3,
        "stimulus": stimulus_instance_3,
        "time_submitted": "2024-11-17T19:12:00.000Z"
    }
]
for test7_response_3 in test7_response_3:
    Response.objects.create(**test7_response_3)

test7_response_4 = [
    {
        "response": "1356",
        "test": completed_test_7,
        "response_position": 4,
        "stimulus": stimulus_instance_4,
        "time_submitted": "2024-11-17T19:13:00.000Z"
    }
]
for test7_response_4 in test7_response_4:
    Response.objects.create(**test7_response_4)

test7_response_5 = [
    {
        "response": "1245",
        "test": completed_test_7,
        "response_position": 5,
        "stimulus": stimulus_instance_5,
        "time_submitted": "2024-11-17T19:13:00.000Z"
    }
]
for test7_response_5 in test7_response_5:
    Response.objects.create(**test7_response_5)

test7_response_6 = [
    {
        "response": "12345",
        "test": completed_test_7,
        "response_position": 6,
        "stimulus": stimulus_instance_6,
        "time_submitted": "2024-11-17T19:13:00.000Z"
    }
]
for test7_response_6 in test7_response_6:
    Response.objects.create(**test7_response_6)

test7_response_7 = [
    {
        "response": "1346",
        "test": completed_test_7,
        "response_position": 7,
        "stimulus": stimulus_instance_7,
        "time_submitted": "2024-11-17T19:14:00.000Z"
    }
]
for test7_response_7 in test7_response_7:
    Response.objects.create(**test7_response_7)

test7_response_8 = [
    {
        "response": "12345",
        "test": completed_test_7,
        "response_position": 8,
        "stimulus": stimulus_instance_8,
        "time_submitted": "2024-11-17T19:14:00.000Z"
    }
]
for test7_response_8 in test7_response_8:
    Response.objects.create(**test7_response_8)

test7_response_9 = [
    {
        "response": "56KR",
        "test": completed_test_7,
        "response_position": 9,
        "stimulus": stimulus_instance_9,
        "time_submitted": "2024-11-17T19:14:00.000Z"
    }
]
for test7_response_9 in test7_response_9:
    Response.objects.create(**test7_response_9)

test7_response_10 = [
    {
        "response": "346LY",
        "test": completed_test_7,
        "response_position": 10,
        "stimulus": stimulus_instance_10,
        "time_submitted": "2024-11-17T19:15:00.000Z"
    }
]
for test7_response_10 in test7_response_10:
    Response.objects.create(**test7_response_10)

test7_response_11 = [
    {
        "response": "56FP",
        "test": completed_test_7,
        "response_position": 11,
        "stimulus": stimulus_instance_11,
        "time_submitted": "2024-11-17T19:15:00.000Z"
    }
]
for test7_response_11 in test7_response_11:
    Response.objects.create(**test7_response_11)

test7_response_12 = [
    {
        "response": "25RY",
        "test": completed_test_7,
        "response_position": 12,
        "stimulus": stimulus_instance_12,
        "time_submitted": "2024-11-17T19:15:00.000Z"
    }
]
for test7_response_12 in test7_response_12:
    Response.objects.create(**test7_response_12)

test7_response_13 = [
    {
        "response": "56LP",
        "test": completed_test_7,
        "response_position": 13,
        "stimulus": stimulus_instance_13,
        "time_submitted": "2024-11-17T19:15:00.000Z"
    }
]
for test7_response_13 in test7_response_13:
    Response.objects.create(**test7_response_13)

test7_response_14 = [
    {
        "response": "134FR",
        "test": completed_test_7,
        "response_position": 14,
        "stimulus": stimulus_instance_14,
        "time_submitted": "2024-11-17T19:16:00.000Z"
    }
]
for test7_response_14 in test7_response_14:
    Response.objects.create(**test7_response_14)

test7_response_15 = [
    {
        "response": "136RY",
        "test": completed_test_7,
        "response_position": 15,
        "stimulus": stimulus_instance_15,
        "time_submitted": "2024-11-17T19:16:00.000Z"
    }
]
for test7_response_15 in test7_response_15:
    Response.objects.create(**test7_response_15)

test7_response_16 = [
    {
        "response": "246KP",
        "test": completed_test_7,
        "response_position": 16,
        "stimulus": stimulus_instance_16,
        "time_submitted": "2024-11-17T19:16:00.000Z"
    }
]
for test7_response_16 in test7_response_16:
    Response.objects.create(**test7_response_16)

test8_response_1 = [
    {
        "response": "2456",
        "test": completed_test_8,
        "response_position": 1,
        "stimulus": stimulus_instance_1,
        "time_submitted": "2024-11-17T19:27:00Z"
    }
]
for test8_response_1 in test8_response_1:
    Response.objects.create(**test8_response_1)

test8_response_2 = [
    {
        "response": "23456",
        "test": completed_test_8,
        "response_position": 2,
        "stimulus": stimulus_instance_2,
        "time_submitted": "2024-11-17T19:27:00Z"
    }
]
for test8_response_2 in test8_response_2:
    Response.objects.create(**test8_response_2)

test8_response_3 = [
    {
        "response": "2346",
        "test": completed_test_8,
        "response_position": 3,
        "stimulus": stimulus_instance_3,
        "time_submitted": "2024-11-17T19:27:00Z"
    }
]
for test8_response_3 in test8_response_3:
    Response.objects.create(**test8_response_3)

test8_response_4 = [
    {
        "response": "1356",
        "test": completed_test_8,
        "response_position": 4,
        "stimulus": stimulus_instance_4,
        "time_submitted": "2024-11-17T19:27:00Z"
    }
]
for test8_response_4 in test8_response_4:
    Response.objects.create(**test8_response_4)

test8_response_5 = [
    {
        "response": "1245",
        "test": completed_test_8,
        "response_position": 5,
        "stimulus": stimulus_instance_5,
        "time_submitted": "2024-11-17T19:27:00Z"
    }
]
for test8_response_5 in test8_response_5:
    Response.objects.create(**test8_response_5)

test8_response_6 = [
    {
        "response": "12345",
        "test": completed_test_8,
        "response_position": 6,
        "stimulus": stimulus_instance_6,
        "time_submitted": "2024-11-17T19:28:00Z"
    }
]
for test8_response_6 in test8_response_6:
    Response.objects.create(**test8_response_6)

test8_response_7 = [
    {
        "response": "13456",
        "test": completed_test_8,
        "response_position": 7,
        "stimulus": stimulus_instance_7,
        "time_submitted": "2024-11-17T19:28:00Z"
    }
]
for test8_response_7 in test8_response_7:
    Response.objects.create(**test8_response_7)

test8_response_8 = [
    {
        "response": "12345",
        "test": completed_test_8,
        "response_position": 8,
        "stimulus": stimulus_instance_8,
        "time_submitted": "2024-11-17T19:28:00Z"
    }
]
for test8_response_8 in test8_response_8:
    Response.objects.create(**test8_response_8)

test8_response_9 = [
    {
        "response": "56KR",
        "test": completed_test_8,
        "response_position": 9,
        "stimulus": stimulus_instance_9,
        "time_submitted": "2024-11-17T19:28:00Z"
    }
]
for test8_response_9 in test8_response_9:
    Response.objects.create(**test8_response_9)

test8_response_10 = [
    {
        "response": "346LY",
        "test": completed_test_8,
        "response_position": 10,
        "stimulus": stimulus_instance_10,
        "time_submitted": "2024-11-17T19:29:00Z"
    }
]
for test8_response_10 in test8_response_10:
    Response.objects.create(**test8_response_10)

test8_response_11 = [
    {
        "response": "56FP",
        "test": completed_test_8,
        "response_position": 11,
        "stimulus": stimulus_instance_11,
        "time_submitted": "2024-11-17T19:29:00Z"
    }
]
for test8_response_11 in test8_response_11:
    Response.objects.create(**test8_response_11)

test8_response_12 = [
    {
        "response": "25RY",
        "test": completed_test_8,
        "response_position": 12,
        "stimulus": stimulus_instance_12,
        "time_submitted": "2024-11-17T19:29:00Z"
    }
]
for test8_response_12 in test8_response_12:
    Response.objects.create(**test8_response_12)

test8_response_13 = [
    {
        "response": "56LP",
        "test": completed_test_8,
        "response_position": 13,
        "stimulus": stimulus_instance_13,
        "time_submitted": "2024-11-17T19:29:00Z"
    }
]
for test8_response_13 in test8_response_13:
    Response.objects.create(**test8_response_13)

test8_response_14 = [
    {
        "response": "136LY",
        "test": completed_test_8,
        "response_position": 14,
        "stimulus": stimulus_instance_14,
        "time_submitted": "2024-11-17T19:29:00Z"
    }
]
for test8_response_14 in test8_response_14:
    Response.objects.create(**test8_response_14)

test8_response_15 = [
    {
        "response": "136RY",
        "test": completed_test_8,
        "response_position": 15,
        "stimulus": stimulus_instance_15,
        "time_submitted": "2024-11-17T19:30:00Z"
    }
]
for test8_response_15 in test8_response_15:
    Response.objects.create(**test8_response_15)

test8_response_16 = [
    {
        "response": "246KP",
        "test": completed_test_8,
        "response_position": 16,
        "stimulus": stimulus_instance_16,
        "time_submitted": "2024-11-17T19:30:00Z"
    }
]
for test8_response_16 in test8_response_16:
    Response.objects.create(**test8_response_16)



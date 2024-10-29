from django.contrib.auth.models import User
from website.models import Test, Ticket
from django.utils import timezone

# Delete existing users, tests, and tickets
User.objects.all().delete()
Test.objects.all().delete()
Ticket.objects.all().delete()

# Create superuser 'admin' with password 'password'
User.objects.create_superuser(username='admin', password='password', email='admin@example.com')

# Create additional user 'DoctorWho' with password '@password115'
doctor_who = User.objects.create_user(username='DoctorWho', password='@password115')

# Create a Test instance associated with DoctorWho
test = Test.objects.create(
    user=doctor_who,
    age=35,  # Example age, adjust as needed
    created_at=timezone.now()
)

# Create a Ticket instance submitted by DoctorWho
ticket = Ticket.objects.create(
    user=doctor_who,
    category='general',  # Example category, can be changed
    description="This is a sample issue reported by DoctorWho.",
    created_at=timezone.now()
)
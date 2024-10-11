from django.contrib.auth.backends import BaseBackend
from .models import User

class CustomUserBackend(BaseBackend):  # Inherit from BaseBackend
    def authenticate(self, request, uname=None, passwd=None, **kwargs):
        try:
            user = User.objects.get(uname=uname)
            print(f"User found: {user.uname}")  # Debug: Check found user
            print(f"Password provided: {passwd}")  # Debug: Password entered
            print(f"Stored password: {user.passwd}")  # Debug: Password in DB

            # Direct comparison of password without hashing
            if passwd == user.passwd:
                return user
            else:
                print("Password check failed.")  # Debug: Password mismatch
                return None

        except User.DoesNotExist:
            print("User does not exist.")  # Debug: User not found
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

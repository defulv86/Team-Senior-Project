# forms.py
from django import forms
from django.contrib.auth.models import User
from .validate import validate_org_email

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        # Validate the username to ensure it's unique
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already in use.")
        return username

    def clean_email(self):
        # Validate the email ends in .org
        email = self.cleaned_data.get('email')
        validate_org_email(email)
        
        # Ensure the email is unique
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean(self):
        # Validate that the password and confirm password match
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

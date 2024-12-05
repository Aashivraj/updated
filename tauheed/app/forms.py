from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    
    class Meta:
        model = UserData
        fields = [
            'first_name', 'last_name', 'username', 'email', 'gender', 'date_of_birth',
            'parent_name', 'parent_surname', 'parent_phone_number', 'school_college_or_employment',
            'diversity', 'photo_consent', 'term_and_condition_gdpr', 'password1', 'password2', 'discount_card'
        ]
        
    def clean(self):
        cleaned_data = super().clean()

        # Required fields validation
        required_fields = [
            'first_name', 'email', 'gender', 'photo_consent', 'term_and_condition_gdpr'
        ]
        
        # Checking if the required fields are empty
        for field in required_fields:
            value = cleaned_data.get(field)
            if not value:
                self.add_error(field, f"{field.replace('_', ' ').capitalize()} cannot be empty.")
        
        # Password validation (ensure both passwords match)
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

        return cleaned_data


# Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')



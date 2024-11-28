from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm



from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import UserData  # Assuming your model is UserData

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    
    class Meta:
        model = UserData
        fields = [
            'first_name', 'last_name', 'username', 'email', 'gender', 'date_of_birth',
            'parent_name', 'parent_surname', 'parent_phone_number', 'school_college_or_employment',
            'diversity', 'photo_consent', 'term_and_condition_gdpr', 'password1', 'password2'
        ]
    
    def clean(self):
        cleaned_data = super().clean()

        # Check for empty required fields
        required_fields = [
            'first_name', 'last_name', 'username', 'email', 'gender', 'date_of_birth',
            'parent_name', 'parent_surname', 'parent_phone_number', 'school_college_or_employment',
            'diversity', 'photo_consent', 'term_and_condition_gdpr'
        ]
        
        for field in required_fields:
            value = cleaned_data.get(field)
            if not value:
                self.add_error(field, f"{field.replace('_', ' ').capitalize()} cannot be empty.")
        
        # Password validation
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")
        
        return cleaned_data

# Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')


class AddStaffForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = UserData
        fields = ['first_name','username', 'last_name', 'email', 'password', 'is_active']

    def save(self, commit=True):
        staff = super().save(commit=False)
        staff.password = make_password(self.cleaned_data['password'])  # Hash the password here
        if commit:
            staff.save()
        return staff
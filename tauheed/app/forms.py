import re
from django import forms
from .models import *
from django.contrib.auth.hashers import make_password, check_password



class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = [
            'first_name', 'last_name', 'username', 'email', 'gender', 'date_of_birth', 
            'password', 'parent_name', 'parent_phone_number', 'parent_surname', 
            'school_college_or_employment', 'diversity', 'photo_consent', 'term_and_condition_gdpr'
        ]

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    def save(self, commit=True):
        # Get the cleaned data from the form
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')

        # Hash the password before saving it
        cleaned_data['password'] = make_password(password)

        # Create a UserData instance with the cleaned data
        user = super().save(commit=False)

        # Set the hashed password to the user instance
        user.password = cleaned_data['password']

        # Save the user instance
        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


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
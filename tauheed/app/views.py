from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from .filters import * 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the new user data
            user = form.save(commit=False)
            user.join_type = '3'
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:  # Check if passwords match
                user.set_password(password1)  # Hash the password
                user.save()
                # Optionally log the user in after successful registration
                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect('login')  # Redirect to a homepage or login page
            else:
                messages.error(request, "Passwords do not match.")
        else:
            # Add all form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


# Login View
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        # Debugging: Check form validity and errors
        print(form.is_valid())  # Should print True if the form is valid
        print(form.errors)  # Check for any specific errors

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                # Fetch the user from the database based on the username
                user = UserData.objects.get(username=username)
                
                # Check if the password is correct
                if user.check_password(password):
                    # Log the user in
                    login(request, user)
                    
                    # Redirect based on user type (Admin, Staff, or User)
                    if request.user.is_superuser:  # Admin
                        return redirect('dashboard')
                    elif request.user.join_type == '2':  # Staff
                        return redirect('#')  # Replace with your staff dashboard URL
                    elif request.user.join_type == '3':  # User
                        return redirect('frontend_dashboard')  # Replace with the user-specific URL
                    
                else:
                    messages.error(request, 'Invalid username or password')
            
            except UserData.DoesNotExist:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def frontend_dashboard(request):
    return render(request, "frontend_dashboard.html")


def logout_view(request):
    if "user_id" in request.session:
        del request.session["user_id"]
        del request.session["username"]
    messages.success(request, "You have successfully logged out.")
    return redirect("login")




def add_staff(request):
    
    if request.method == "POST":
        form = AddStaffForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.user_type = 'BACK_STAFF_USER'  # Set user type to Back Staff
            staff.save()

            messages.success(request, "Staff member added successfully!")
            return redirect('add_staff') 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AddStaffForm()

    return render(request, "add_staff.html", {"form": form})



def dashboard(request):
    if request.method == "GET":
        return render(request, "dashboard.html")
        # return render(request, "frontend_dashboard.html")
    
    else:
        print("wrong")
    return render (request, "login.html" )



def backstaff_user_list(request):
    # Get all users with 'BACK_STAFF_USER' role
    queryset = UserData.objects.filter(user_type='BACK_STAFF_USER')
    
    # Apply filters
    user_filter = UserFilter(request.GET, queryset=queryset)
    
    return render(request, 'backstaff_user.html', {'filter': user_filter})

def user_list(request):
    # Get all users with 'USER' role
    queryset = UserData.objects.filter(user_type='USER')
    
    # Apply filters
    user_filter = UserFilter(request.GET, queryset=queryset)
    
    return render(request, 'user_list.html', {'filter': user_filter})
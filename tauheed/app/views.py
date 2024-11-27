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
            form.save()
            messages.success(request, "Registration successful!")
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            messages.error(request, "There were errors in your form. Please check.")
    else:
        form = UserRegistrationForm()
    
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = UserData.objects.get(username=username)
            except UserData.DoesNotExist:
                user = None
                

            if user and check_password(password, user.password):
                if user.is_active:
                    login(request, user)
                    if request.user.is_superuser:
                        return redirect('dashboard')  # Redirect superusers
                    else:
                        return redirect('frontend_dashboard')  # Redirect regular users
                else:
                    messages.error(request, "Account is disabled.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
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
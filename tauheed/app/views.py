from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

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
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            # Get the user from the UserData model
            user = UserData.objects.get(username=username)

            # Check if the password matches
            if check_password(password, user.password):
                # Mark the user as authenticated for session management
                
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password.")
        except UserData.DoesNotExist:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def logout_view(request):
    if "user_id" in request.session:
        del request.session["user_id"]
        del request.session["username"]
    messages.success(request, "You have successfully logged out.")
    return redirect("login")



@login_required
def add_staff(request):
    # Restrict access to admin users only
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to add staff.")
        return redirect('dashboard')  # Replace 'dashboard' with the appropriate URL name
    
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


@login_required
def dashboard(request):
    if request.method == "GET":
        return render(request, "dashboard.html")
        # return render(request, "frontend_dashboard.html")
    
    else:
        print("wrong")
    return render (request, "login.html" )


@login_required
def user_list(request):
    # Get all users with 'USER' role
    users = UserData.objects.filter(user_type='BACK_STAFF_USER')
    
    return render(request, 'user_list.html', {'users': users})
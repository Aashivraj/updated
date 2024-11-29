from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import * 
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
                        return redirect('#')
                    elif request.user.join_type == '2':  # Staff
                        return redirect('#')  # Replace with your staff dashboard URL
                    elif request.user.join_type == '3':  # User
                        return redirect('dashboard')  # Replace with the user-specific URL
                    
                else:
                    messages.error(request, 'Invalid username or password')
            
            except UserData.DoesNotExist:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})



def logout_view(request):
    if "user_id" in request.session:
        del request.session["user_id"]
        del request.session["username"]
    messages.success(request, "You have successfully logged out.")
    return redirect("login")



def dashboard(request):
    if request.method == "GET":
        return render(request, "dashboard.html")
    
    else:
        print("wrong")
    return render (request, "login.html" )


from django.shortcuts import render
from .models import Sport  # Assuming the Sport model exists and has a 'name' field

def listing(request):
    if request.method == "GET":
        # Fetch sports from the database
        sports = Sport.objects.values_list('name', flat=True)

        # Get the selected sport from the query parameter
        selected_sport = request.GET.get('sport', None)

        # Debugging logs (check if these values are fetched correctly)
        print(f"Sports: {list(sports)}")  # Convert QuerySet to list for readability
        print(f"Selected Sport: {selected_sport}")

        return render(request, "listing.html", {"sports": sports, "selected_sport": selected_sport})
    else:
        print("wrong")
        return render(request, "login.html")

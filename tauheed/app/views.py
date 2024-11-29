from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import * 
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import datetime
from django.utils.timezone import make_aware


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the new user data
            user = form.save(commit=False)
            user.join_type = '3'
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2: 
                user.set_password(password1)  
                user.save()
                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect('login') 
            else:
                messages.error(request, "Passwords do not match.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        


        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = UserData.objects.get(username=username)
                

                if user.check_password(password):
                    login(request, user)
                    

                    if request.user.is_superuser:  
                        return redirect('login')
                    elif request.user.join_type == '2': 
                        return redirect('login')  
                    elif request.user.join_type == '3':  
                        return redirect('dashboard')  
                    
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




def user_profile(request):
    user_data = UserData.objects.get(username=request.user)  # Fetch the data of the logged-in user
    return render(request, 'profile.html', {'user_data': user_data})




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




def confirm_booking(request):
    if request.method == "POST":
        slot_time_str = request.POST.get('slot_time')  
        sport_name = request.POST.get('sport')
        user = request.user  

        try:
            sport = Sport.objects.get(name__iexact=sport_name)
            user_data = UserData.objects.get(username=user.username)
            discount_card = user_data.discount_card
            
            if discount_card == 1:  
                amount = 2  
            else: 
                amount = 4
                
            today = now().date()
            start_time_str = slot_time_str.split(' - ')[0]  # "08:00 AM"
            start_time = datetime.strptime(f"{today} {start_time_str}", "%Y-%m-%d %I:%M %p")
            start_time = make_aware(start_time)  # Convert to timezone-aware datetime

            # Create a new booking
            BookingHistory.objects.create(
                sport=sport,
                booking_date=today, 
                slot_time=start_time, 
                user=user,
                amount=amount ,  
                payment_status='Completed',
                booking_status=True
            )
            
            messages.success(request, f"Booking for {sport_name} at {slot_time_str} confirmed!")
            return redirect('dashboard') 
        except Sport.DoesNotExist:
            messages.error(request, "Invalid sport selected.")
            return redirect('listing')  

    messages.error(request, "Invalid request.")
    return redirect('listing')




def booking_list(request):
   
    booking_history = BookingHistory.objects.filter(user=request.user).order_by('-booking_date') 
    
    return render(request, 'booking_history.html', {'history': booking_history})
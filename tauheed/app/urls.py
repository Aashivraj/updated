from django.urls import path
from .views import *

urlpatterns = [
    
    path("register/", register, name="register"),
    path("", login_user, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("listing/", listing, name="listing"),

    path('profile/', user_profile, name='profile'),
    
    

    path('confirm-booking/', confirm_booking, name='confirm_booking'),
    path('booking_list/', booking_list, name='booking_list'),
    
    path('cancel_membership/', cancel_membership, name='cancel_membership'),
]

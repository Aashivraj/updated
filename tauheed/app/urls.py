from django.urls import path
from .views import *

urlpatterns = [
    
    path("register/", register, name="register"),
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("frontend_dashboard/", frontend_dashboard, name="frontend_dashboard"),
    
    path("add_staff/", add_staff, name="add_staff"),
    
    
    path('user_list/', user_list, name='user_list'),
    path('backstaff_user_list/', backstaff_user_list, name='backstaff_user_list'),
]

from django.urls import path
from .views import *

urlpatterns = [
    
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    
    path("add_staff/", add_staff, name="add_staff"),
    
    
    path('user_list/', user_list, name='user_list'),
]

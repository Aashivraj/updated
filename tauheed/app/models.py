from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# class BackOfficeStaff(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=50, unique=True)
#     password = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

#     class Meta:
#         db_table = "back_office_staff"


class UserDataManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and return a superuser with an email, username, and password."""
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class UserData(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    

    USER_TYPE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
        ('BACK_STAFF_USER', 'Back_Staff_User')
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=False, null=True)
    email = models.EmailField(max_length=50, unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=25, default='USER')

    date_of_birth = models.DateField(blank=True, null=True)
    parent_name = models.CharField(max_length=50)
    parent_surname = models.CharField(max_length=100)
    parent_phone_number = models.CharField(max_length=20)
    school_college_or_employment = models.CharField(max_length=100)
    diversity = models.CharField(max_length=100)
    photo_consent = models.BooleanField(default=False)
    term_and_condition_gdpr = models.BooleanField(default=False)
    discount_card = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)  

    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(null=True, blank=True)

    # Reverse relationships
    groups = models.ManyToManyField(
        'auth.Group', related_name='user_data_set', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='user_data_set', blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserDataManager()

    def save(self, *args, **kwargs):
        if not self.last_login:
            self.last_login = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        db_table = "users"

class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "sports"


class BookingHistory(models.Model):
    PAYMENT_METHODS = (
        ('1', 'Cash'),
        ('2', 'Credit Card'),
        ('3', "Wep"),
    )   
    
    payment_methods = models.CharField(choices=PAYMENT_METHODS, max_length=25)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateField()
    slot_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name="booking_history")

    def __str__(self):
        return f"Booking by {self.user.username} - {self.sport.name} on {self.booking_date}"

    class Meta:
        db_table = "booking_history"
        
        
        

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserData(AbstractUser):
    USER_TYPE_CHOICES = (
        ('1', 'Admin'),
        ('2', 'Staff'),
        ('3', 'User'),
    )
    EDUCATION_EMPLOYMENT_CHOICES = (
        ('SCHOOL', 'School'),
        ('COLLEGE', 'College'),
        ('EMPLOYMENT', 'Employment'),
    )

    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)
    join_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=1, default='3')  # User type
    date_of_birth = models.DateField(blank=True, null=True)
    parent_name = models.CharField(max_length=50)
    parent_surname = models.CharField(max_length=100)
    parent_phone_number = models.CharField(max_length=20)
    school_college_or_employment = models.CharField(choices=EDUCATION_EMPLOYMENT_CHOICES, max_length=20)
    diversity = models.CharField(max_length=100)
    photo_consent = models.BooleanField(default=False)
    term_and_condition_gdpr = models.BooleanField(default=False)
    discount_card = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.join_type = '1'  # Admin
        super(UserData, self).save(*args, **kwargs)
    
    # Ensure that superuser always gets 'join_type' as '1' when created
    @classmethod
    def _create_user(cls, username, email, password=None, **extra_fields):
        """
        Create and return a user with an email, username and password.
        """
        if extra_fields.get('is_superuser'):
            extra_fields['join_type'] = '1'  # Admin join_type for superusers
        return super()._create_user(username, email, password, **extra_fields)
    
    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"


class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "sports"


class BookingHistory(models.Model):

    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateField()
    slot_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name="booking_history")
    amount = models.IntegerField()

    def __str__(self):
        return f"Booking by {self.user.username} - {self.sport.name} on {self.booking_date}"

    class Meta:
        db_table = "booking_history"
        
        
        

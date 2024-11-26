from django.db import models


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


class UserData(models.Model):
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
    password = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=50)
    parent_surname = models.CharField(max_length=100)
    parent_phone_number = models.CharField(max_length=20)
    school_college_or_employment = models.CharField(max_length=100)
    diversity = models.CharField(max_length=100)
    photo_consent = models.BooleanField(default=False)
    term_and_condition_gdpr = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

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

    def __str__(self):
        return f"Booking by {self.user.username} - {self.sport.name} on {self.booking_date}"

    class Meta:
        db_table = "booking_history"

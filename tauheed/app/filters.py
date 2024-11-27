import django_filters
from .models import UserData

class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', label="First Name")
    last_name = django_filters.CharFilter(lookup_expr='icontains', label="Last Name")
    email = django_filters.CharFilter(lookup_expr='icontains', label="Email")

    class Meta:
        model = UserData
        fields = ['first_name', 'last_name', 'email']

import django_filters

from core.models import *

class CarFilter(django_filters.FilterSet):
    price_from = django_filters.NumberFilter(lookup_expr='gte', field_name='price')
    price_to = django_filters.NumberFilter(lookup_expr='lte', field_name='price')
    class Meta:
        model = Car
        fields = ['madel', 'registration','generation', 'region', 'city', 'type', 'drive', 'gear', 'fuel', 'price_from', 'price_to','in_stock', 'exchange', 'state', 'rudder']
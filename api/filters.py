import django_filters

from core.models import Car, Country

class CarFilter(django_filters.FilterSet):
    price_from = django_filters.NumberFilter(lookup_expr='gte', field_name='price')
    price_to = django_filters.NumberFilter(lookup_expr='lte', field_name='price')
    registration = django_filters.ModelMultipleChoiceFilter(queryset=Country.objects.all())

    class Meta:
        model = Car
        fields = ['registration', 'type', 'user', 'drive', 'gear', 'fuel']
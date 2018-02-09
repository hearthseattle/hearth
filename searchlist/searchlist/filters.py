from .models import Resource
import django_filters


class ResourceFilter(django_filters.FilterSet):
    """Filter to filter down results."""
    upper_age = django_filters.NumberFilter(name='upper_age', lookup_expr='gte')
    lower_age = django_filters.NumberFilter(name='lower_age', lookup_expr='lte')
    languages__languages = django_filters.CharFilter(name='languages__languages')
    services__services = django_filters.CharFilter(name='services__services')

    class Meta:
        model = Resource
        fields = ['upper_age', 'lower_age', 'gender', 'services__services',
                  'languages__languages', 'accepts_criminal_records',
                  'pets', 'sober_only', 'open_24_hours', 'family_friendly',
                  'orca_cards_available', 'accepts_incarcerated']

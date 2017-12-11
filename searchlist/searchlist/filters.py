from .models import Resource
import django_filters


class ResourceFilter(django_filters.FilterSet):
    """Filter to filter down results."""
    upper_age = django_filters.NumberFilter(name='upper_age', lookup_expr='lte')
    lower_age = django_filters.NumberFilter(name='lower_age', lookup_expr='gte')

    class Meta:
        model = Resource
        fields = ['upper_age', 'lower_age', 'gender', 'services',
                  'languages', 'accepts_criminals', 'service_animals', 'pets',
                  'sober_only', 'open_24_hours', 'family_friendly',
                  'orca_cards_available', 'accepts_incarcerated']

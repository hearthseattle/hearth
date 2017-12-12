from .models import Resource
import django_filters


class ResourceFilter(django_filters.FilterSet):
    """Filter to filter down results."""
    upper_age = django_filters.NumberFilter(name='upper_age', lookup_expr='lte')
    lower_age = django_filters.NumberFilter(name='lower_age', lookup_expr='gte')
    languages__languages = django_filters.CharFilter(name='languages__languages', lookup_expr='in')
    services__services = django_filters.CharFilter(name='services__services', lookup_expr='in')

    class Meta:
        model = Resource
        fields = ['upper_age', 'lower_age', 'gender', 'services__services',
                  'languages__languages', 'accepts_criminals', 'service_animals',
                  'pets', 'sober_only', 'open_24_hours', 'family_friendly',
                  'orca_cards_available', 'accepts_incarcerated']

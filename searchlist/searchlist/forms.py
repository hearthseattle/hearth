"""File containing the form for the edit/creation views."""
from django.forms import ModelForm
from .models import Resource
from localflavor.us.forms import USStateSelect


class ResourceForm(ModelForm):
    """Form for editing and creating resources."""

    class Meta:
        model = Resource
        fields = ['main_category', 'org_name',
                  'description', 'street', 'city', 'state', 'zip_code', 'website',
                  'phone_number', 'image', 'tags']
        labels = {
            'org_name': 'Name of Organization',
            'main_category': 'Main Categories',
        }
        help_texts = {
            'main_category': 'The core services your organization provides.',
        }
        widgets = {
            'state': USStateSelect(attrs={'disabled': True}),
        }

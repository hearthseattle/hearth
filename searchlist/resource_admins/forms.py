from search.models import Resource
from django import forms


class ResourceForm(forms.ModelForm):
    """Build a form for the administrator to add resources
    within the site.
    """

    class Meta:
        """Model the form is based on."""

        model = Resource
        fields = []

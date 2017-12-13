"""File containing the form for the edit/creation views."""
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.forms import (
    ModelForm,
    Form
)
from .models import Resource, SERVICES


class ResourceForm(ModelForm):
    """Form for editing and creating resources."""

    states = forms.ChoiceField(
        choices=[('Washington', 'Washington')],
        initial='Washington',
        disabled=True,
        label='State'
    )

    website = forms.URLField(initial='http://')

    class Meta:
        model = Resource
        fields = ['name', 'description', 'street', 'city', 'states',
                  'zip_code', 'website', 'phone_number', 'image', 'gender',
                  'languages', 'services', 'lower_age', 'upper_age',
                  'us_citizens_only', 'sober_only', 'case_managers',
                  'open_24_hours',
                  'service_animals', 'pets', 'accepts_sex_offenders',
                  'accepts_criminals', 'accepts_incarcerated',
                  'family_friendly', 'orca_cards_available']
        widgets = {
            'languages': forms.CheckboxSelectMultiple(),
            'services': forms.CheckboxSelectMultiple()
        }
        labels = {
            'languages': 'Languages spoken other than English?',
            'services': 'Select all services your organization provides.',
            'gender': 'Gender restrictions?',
            'lower_age': 'Lower age limit',
            'upper_age': 'Upper age limit'
        }

    def clean(self):
        """Overridden clean method for validation of the age inputs."""
        if self.cleaned_data['upper_age'] <= self.cleaned_data['lower_age']:
            raise ValidationError(
                'Invalid entries for lower and upper age ranges.'
            )
        return self.cleaned_data


class FilterForm(Form):
    """Form for the filtering of resources on the home page."""
    age = forms.IntegerField()
    gender = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect(),
        choices=[
            ('M', 'Male'),
            ('W', 'Female'),
            ('A', 'LGBTQIA')
        ],
        label='Gender'
    )
    services__services = forms.ChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(),
        choices=zip(SERVICES, SERVICES.copy()),
        label='Services'
        )
    languages__languages = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        choices=[
            ('English', 'English'),
            ('Spanish', 'Spanish'),
            ('Russian', 'Russian'),
            ('Ukrainian', 'Ukrainian'),
            ('German', 'German'),
            ('French', 'French'),
            ('Somali', 'Somali'),
            ('Vietnamese', 'Vietnamese'),
            ('Chinese', 'Chinese')
        ],
        label='Languages spoken'
    )

    accepts_criminals = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxInput(),
        choices=[
            (True, 'Yes'),
        ],
        label='Criminal Record'
    )

    service_animals = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxInput(),
        choices=[
            (True, 'Yes'),
        ],
        label='Service animal'
    )

    pets = forms.BooleanField(
        required=False,
        label='Pets'
    )

    sober_only = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxInput(),
        choices=[
            (True, 'Yes')
        ],
        label='Sober'
    )

    open_24_hours = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxInput(),
        choices=[
            (True, 'Yes'),
        ],
        label='Open 24 hours'
    )

    family_friendly = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxInput(),
        label='Family')

    orca_cards_available = forms.BooleanField(
        required=False,
        label='Orca cards'
        )
    accepts_incarcerated = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxInput(),
        label='Incarcerated'
        )

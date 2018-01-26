"""File containing the form for the edit/creation views."""
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.forms import (
    ModelForm,
    Form
)
from .models import Resource, SERVICES
from localflavor.us.forms import (
    USPhoneNumberField,
    USZipCodeField
)


class ResourceForm(ModelForm):
    """Form for editing and creating resources."""

    state = forms.ChoiceField(
        choices=[('Washington', 'Washington')],
        initial='Washington',
        disabled=True,
        label='State'
    )

    street = forms.CharField(required=False)

    zip_code = USZipCodeField(required=False)

    phone_number = USPhoneNumberField(required=False)

    fax_number = USPhoneNumberField(required=False)

    website = forms.URLField(initial='http://', required=False)

    class Meta:
        model = Resource
        fields = ['name', 'description', 'street', 'city', 'state',
                  'zip_code', 'website', 'phone_number', 'fax_number', 'email', 'image', 'gender',
                  'languages', 'services', 'lower_age', 'upper_age',
                  'us_citizens_only', 'sober_only', 'case_managers',
                  'open_24_hours', 'pets', 'accepts_sex_offender_records',
                  'accepts_criminal_records', 'accepts_incarcerated',
                  'family_friendly', 'orca_cards_available']
        widgets = {
            'languages': forms.CheckboxSelectMultiple(),
            'services': forms.CheckboxSelectMultiple()
        }
        labels = {
            'languages': 'Languages spoken:',
            'services': 'Select all services your organization provides.',
            'gender': 'Gender restrictions?',
            'lower_age': 'Lower age limit',
            'upper_age': 'Upper age limit',
            'pets': 'Pets allowed'
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

    pets = forms.BooleanField(
        required=False,
        label='Pets Allowed'
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

"""File containing the form for the edit/creation views."""
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.forms import (
    ModelForm,
    Form
)
from .models import Resource
import os
import pickle

zips = pickle.load(open(os.path.join(settings.BASE_DIR, '../zips.p'), "rb"))


def validate_zip(zip_code):
    """Ensure zip provided by user is in King County."""
    if zip_code not in zips:
        raise ValidationError(
            '{} is not a valid King County zip code.'.format(zip_code),
            params={'zip_code': zip_code},
        )


class ResourceForm(ModelForm):
    """Form for editing and creating resources."""

    states = forms.ChoiceField(
        choices=[('Washington', 'Washington')],
        initial='Washington',
        disabled=True,
        label='State'
    )

    website = forms.URLField(initial='http://')

    zip_code = forms.IntegerField(
        validators=[validate_zip]
    )

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

    gender = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect(),
        choices=[
            ('women', 'Male'),  # Remove any elements with 'women'
            ('men', 'Female'),  # See above comment
            ('no_lgbtqia', 'LGBTQIA')  # See above
        ],
        label='Gender'
    )

    languages = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        choices=[
            ('spanish', 'Spanish'),
            ('russian', 'Russian'),
            ('ukrainian', 'Ukrainian'),
            ('german', 'German'),
            ('french', 'French'),
            ('somali', 'Somali'),
            ('vietnamese', 'Vietnamese'),
            ('chinese', 'Chinese')
        ],
        label='Languages Spoken (other than English)'
    )

    criminal_record = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxInput(),
        choices=[
            ('criminal_record', 'Yes'),  # Remove
        ],
        label='Criminal Record'
    )

    service_animal = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxInput(),
        choices=[
            ('no_pets', 'Yes'),  # Remove
        ],
        label='Service Animal'
    )

    pets = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxInput(),
        choices=[
            ('pets', 'Yes'),  # Add
        ],
        label='Pets'
    )

    sober = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxInput(),
        choices=[
            ('sober', 'Yes')
        ],
        label='Sober'
    )

    open_24 = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxInput(),
        choices=[
            ('24', 'Yes'),  # show
        ],
        label='Open 24 Hours'
    )

    disability = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        choices=[
            ('learning', 'Learning'),
            ('mental', 'Mental'),
            ('physical', 'Physical'),
        ],
        label='Disability'
    )

    nearby = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect(),
        choices=[
            ('.3', '.3 miles'),
            ('5', '5 miles'),
            ('10', '10 miles'),
            ('20', '20 miles'),
        ]
    )

    hours_range = forms.TimeField(
        required=False,
        label='Hours Open'
    )

    incarcerated = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxInput(),
        choices=[
            ('', 'Yes'),
        ],
        label='Currently Incarcerated'
    )

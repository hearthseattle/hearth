"""File containing the form for the edit/creation views."""
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Resource
from localflavor.us.forms import USStateSelect
from localflavor.us.forms import USZipCodeField
import pickle

zips = pickle.load(open('../zips.p', "rb"))


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
    gender = forms.ChoiceField(
        choices=[
            ('any_gender', 'Any'),
            ('women', 'Women Only'),
            ('men', 'Men Only')
        ],
        label='Serve specific genders?'
    )
    age = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=[
            ('no_age', 'No'),
            ('age', 'Yes')
        ],
        label='Age requirements?'
    )
    language = forms.MultipleChoiceField(
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
        label='Languages spoken other than English?',
        required=False
    )
    citizenship = forms.ChoiceField(
        choices=[
            ('any_citizenship', 'All welcome'),
            ('us_citizens_only', 'US Citizens Only')
        ],
        label='Required citizenship status?'
    )
    lgbtqia = forms.ChoiceField(
        choices=[
            ('lgbtqia', 'LGBTQIA welome'),
            ('no_lgbtqia', 'LGBTQIA not accepted')
        ],
        label='LGBTQIA Friendly?'
    )
    sobriety = forms.ChoiceField(
        choices=[
            ('sober', 'Must be sober'),
            ('sober_free', 'Not required to be sober')
        ],
        label='Sobriety requirements?'
    )
    costs = forms.ChoiceField(
        choices=[
            ('free', 'All services free of charge'),
            ('free', 'Some services free of charge'),
            ('not_free', 'No services are free of charge')
        ],
        label='Do you offer services free of charge?'
    )
    case_managers = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'blank': True}),
        choices=[
            ('case_managers', 'Yes'),
            ('no_case_managers', 'No')
        ],
        label='Are case managers available?'
    )
    counselors = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=[
            ('counselors', 'Yes'),
            ('no_counselors', 'No')
        ],
        label='Are counselors available?'
    )
    always_open = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=[
            ('24', 'Yes'),
            ('no_24', 'No')
        ],
        label='Are you open 24 hours?'
    )
    pets = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=[
            ('pets', 'Yes'),
            ('no_pets', 'No'),
            ('service_animals', 'Service animals only')
        ],
        label='Are pets allowed?'
    )
    various = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[
            ('trauma', 'Post trauma'),
            ('trafficking', 'Post human trafficking'),
            ('domestic_violence', 'Post domestic violence'),
            ('legal', 'Legal assistance'),
            ('short_term', 'Short-term housing'),
            ('long_term', 'Long-term housing'),
            ('welfare', 'Welfare assistance'),
            ('meals', 'Meals'),
            ('electronics', 'Electronics'),
            ('transportation', 'Transportation'),
            ('winter', 'Winter Availability'),
            ('storage', 'Storage'),
            ('showers', 'Showers'),
            ('sex_offender', 'Sex offender restrictions'),
            ('criminal_record', 'Criminal record restrictions'),
            ('refugees', 'Refugee assistance'),
        ],
        label='Please select specific services you provide '
              'or additional requirements.'
    )

    class Meta:
        """Meta class for the model."""

        model = Resource
        fields = ['main_category', 'org_name',
                  'description', 'street', 'city',
                  'states',
                  'zip_code', 'website',
                  'phone_number', 'image']
        labels = {
            'org_name': 'Name of Organization',
            'main_category': 'Main Categories',
        }
        help_texts = {
            'main_category': 'The core services your organization provides.',
        }
        # widgets = {
        #     'state': USStateSelect(attrs={'readonly': True}),
        # }

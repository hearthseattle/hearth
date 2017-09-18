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

    zip_code = forms.IntegerField(validators=[validate_zip])
    showers = forms.ChoiceField(choices=[('showers', 'Yes'),
                                         ('no_showers', 'No')],
                                label='Are showers available?')
    gender = forms.ChoiceField(choices=[('any_gender', 'Any'),
                                        ('women', 'Women Only'),
                                        ('men', 'Men Only')],
                               label='Serve specific genders?')
    age = forms.ChoiceField(widget=forms.RadioSelect(),
                            choices=[('no_age', 'No'),
                                     ('age', 'Yes')],
                            label='Age requirements?')
    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                         choices=[('spanish', 'Spanish'),
                                                  ('russian', 'Russian'),
                                                  ('ukrainian', 'Ukrainian'),
                                                  ('german', 'German'),
                                                  ('french', 'French'),
                                                  ('somali', 'Somali'),
                                                  ('vietnamese', 'Vietnamese'),
                                                  ('chinese', 'Chinese')],
                                         label='Languages spoken other than English?')
    citizenship = forms.ChoiceField(choices=[('any_citizenship', 'All welcome'),
                                             ('us_citizens_only', 'US Citizens Only')],
                                    label='Required citizenship status?')
    lgbtqia = forms.ChoiceField(choices=[('lgbtqia', 'LGBTQIA Welome'),
                                         (None, 'LGBTQIA Not Accepted')],
                                label='LGBTQIA Friendly?')

    class Meta:
        model = Resource
        fields = ['main_category', 'org_name',
                  'description', 'street', 'city',
                  'state',
                  'zip_code', 'website',
                  'phone_number', 'image']
        labels = {
            'org_name': 'Name of Organization',
            'main_category': 'Main Categories',
        }
        help_texts = {
            'main_category': 'The core services your organization provides.',
        }
        widgets = {
            'state': USStateSelect(attrs={'readonly': True}),
        }

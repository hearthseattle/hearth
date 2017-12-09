"""Model for search profiles."""
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from localflavor.us.models import (
    USStateField,
    USZipCodeField,
    PhoneNumberField
)


SERVICES = [
    "Medical Care",
    "Housing",
    "Counseling",
    "Citizenship",
    "Job Assistance",
    "Substance Recovery",
    "Fleeing Domestic Violence",
    "Fleeing Human Trafficking",
    "Case Management",
    "Mental Health Treatment",
    "Trauma",
    "Hotline",
    "Welfare",
    "Clothing",
    "Technology",
    "Dental",
    "Pharmacy",
    "Transportation",
    "Winter",
    "Storage",
    "Crisis",
    "Addiction",
    "Childcare",
    "Youth Services",
    "Veteran",
    "Rehabilitation",
    "Mental/Physical Disability",
    "Education",
    "Employment",
    "Financal Assistance",
    "Clothing/Housewares",
    "Food",
    "Healthcare",
    "Shelter",
    "Legal Assistance",
    "Identification",
    "Spiritual"
]


@python_2_unicode_compatible
class Service(models.Model):
    """Model for all services."""

    services = models.CharField(max_length=255)

    def __repr__(self):
        """Display strings, not objects."""
        return self.services

    def __str__(self):
        """Redundant string form."""
        return self.__repr__()


@python_2_unicode_compatible
class Language(models.Model):
    """Model to contain languages."""

    languages = models.CharField(max_length=255)

    def __repr__(self):
        """Display strings, not objects."""
        return self.languages

    def __str__(self):
        """Redundant string form."""
        return self.__repr__()


@python_2_unicode_compatible
class Resource(models.Model):
    """Model for each organization."""

    gender_choices = (
        ('M', 'Men Only'),
        ('W', 'Women Only'),
        ('A', 'Any')
    )
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL,
                                   blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255, default='Seattle')
    state = USStateField(default='WA')
    zip_code = USZipCodeField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    phone_number = PhoneNumberField()
    image = models.ImageField(upload_to='photos', null=True, blank=True)
    gender = models.CharField(
        max_length=255,
        choices=gender_choices,
        default='A'
    )
    services = models.ManyToManyField(Service)
    lower_age = models.PositiveSmallIntegerField(default=0)
    upper_age = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(150)],
        default=150
    )
    languages = models.ManyToManyField(Language)
    us_citizens_only = models.BooleanField()
    sober_only = models.BooleanField()
    case_managers = models.BooleanField()
    open_24_hours = models.BooleanField()
    service_animals = models.BooleanField()
    pets = models.BooleanField()
    accepts_sex_offenders = models.BooleanField()
    accepts_criminals = models.BooleanField()
    accepts_incarcerated = models.BooleanField()
    family_friendly = models.BooleanField(default=False)
    orca_cards_available = models.BooleanField(default=False)

    def __repr__(self):
        """Print org info."""
        return "<[{}] {}, {}>".format(self.id, self.name, self.city)

    def __str__(self):
        """Print organization information."""
        return self.__repr__()

"""Model for search profiles."""
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from localflavor.us.models import (
    USStateField,
    USZipCodeField,
    PhoneNumberField
)

CRISIS = 'CR'
ADDICTION = 'AD'
CHILDCARE = 'CH'
YOUTH = 'YS'
VETERAN = 'VE'
REHAB = 'RE'
DISAB = 'MP'
EDUCATION = 'ED'
EMPLOYMENT = 'EM'
FINANCES = 'FI'
SUPPLIES = 'SU'
FOOD = 'FO'
HEALTH = 'HC'
SHELTER = 'SH'
LEGAL = 'LE'
ID = 'ID'
SPIRITUAL = 'SP'
MEDICAL = 'MD'
HOUSING = 'HS'
COUNSELING = 'CS'
CITIZENSHIP = 'CZ'
JOB = 'JB'
SUBSTANCE = 'SB'
D_VIOLENCE = 'DV'
H_TRAFFICKING = 'HT'
CASE_MANAGEMENT = 'CM'
MENTAL_HEALTH = 'MH'
TRAUMA = 'TR'
HOTLINE = 'HL'
WELFARE = 'WF'
CLOTHING = 'CL'
TECH = 'TE'
DENTAL = 'DT'
PHARMACY = 'PH'
TRANSPORTATION = 'TP'
WINTER = 'WI'
STORAGE = 'ST'

SERVICES = [
    (MEDICAL, "Medical Care"),
    (HOUSING, "Housing"),
    (COUNSELING, "Counseling"),
    (CITIZENSHIP, "Citizenship"),
    (JOB, "Job Assistance"),
    (SUBSTANCE, "Substance Recovery"),
    (D_VIOLENCE, "Fleeing Domestic Violence"),
    (H_TRAFFICKING, "Fleeing Human Trafficking"),
    (CASE_MANAGEMENT, "Case Management"),
    (MENTAL_HEALTH, "Mental Health Treatment"),
    (TRAUMA, "Trauma"),
    (HOTLINE, "Hotline"),
    (WELFARE, "Welfare"),
    (CLOTHING, "Clothing"),
    (TECH, "Technology"),
    (DENTAL, "Dental"),
    (PHARMACY, "Pharmacy"),
    (TRANSPORTATION, "Transportation"),
    (WINTER, "Winter"),
    (STORAGE, "Storage"),
    (CRISIS, "Crisis"),
    (ADDICTION, "Addiction"),
    (CHILDCARE, "Childcare"),
    (YOUTH, "Youth Services"),
    (VETERAN, "Veteran"),
    (REHAB, "Rehabilitation"),
    (DISAB, "Mental/Physical Disability"),
    (EDUCATION, "Education"),
    (EMPLOYMENT, "Employment"),
    (FINANCES, "Financal Assistance"),
    (SUPPLIES, "Clothing/Housewares"),
    (FOOD, "Food"),
    (HEALTH, "Healthcare"),
    (SHELTER, "Shelter"),
    (LEGAL, "Legal Assistance"),
    (ID, "Identification"),
    (SPIRITUAL, "Spiritual")
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

    def __repr__(self):
        """Print org info."""
        return "<[{}] {}, {}>".format(self.id, self.name, self.city)

    def __str__(self):
        """Print organization information."""
        return self.__repr__()

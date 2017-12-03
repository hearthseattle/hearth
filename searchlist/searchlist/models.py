"""Model for search profiles."""
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from localflavor.us.models import (
    USStateField,
    USZipCodeField,
    PhoneNumberField
)
from multiselectfield import MultiSelectField
from taggit.managers import TaggableManager


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


class ResourceTag(models.Model):
    """Tag for related resources."""

    family = models.CharField(max_length=256, db_index=True)
    value = models.CharField(max_length=256)

    def __repr__(self):
        """Helpful representation."""
        return "{}: {}".format(self.family, self.value)

    class Meta:  # noqa: D101
        unique_together = ("family", "value")


class Resource(models.Model):
    """Model for the organization."""

    services = MultiSelectField(
        choices=SERVICES,
        default='None'
    )

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    org_name = models.CharField(max_length=128)
    description = models.TextField()
    street = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, default='Seattle')
    state = USStateField(default='WA')
    zip_code = USZipCodeField(null=True, blank=True)
    website = models.URLField(blank=True)
    phone_number = PhoneNumberField()
    tags = models.ManyToManyField(ResourceTag, blank=True)
    image = models.ImageField(upload_to='photos', null=True, blank=True)

    def __repr__(self):
        """Print org info."""
        return "<[{}] {}, {}>".format(self.id, self.org_name, self.city)

    def __str__(self):
        """Print organization information."""
        return self.__repr__()

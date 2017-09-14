"""Model for search profiles."""
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from localflavor.us.models import (
    USStateField,
    USZipCodeField,
    PhoneNumberField
)
from multiselectfield import MultiSelectField
from taggit.managers import TaggableManager


@python_2_unicode_compatible
class Resource(models.Model):
    """Model for the organization."""
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

    MAIN_CATEGORY = [
        (CRISIS, "Crisis"),
        (ADDICTION, "Addiction"),
        (CHILDCARE, "Childcare"),
        (YOUTH, "Youth Services"),
        (VETERAN, "Veteran"),
        (REHAB, "Rehabilitation"),
        (DISAB, "Mental/Physical Disability"),
        (EDUCATION, "Education"),
        (EMPLOYMENT, "Employment"),
        (FINANCES, "Finances"),
        (SUPPLIES, "Clothing/Housewares"),
        (FOOD, "Food"),
        (HEALTH, "Healthcare"),
        (SHELTER, "Shelter"),
        (LEGAL, "Legal"),
        (ID, "Identification"),
        (SPIRITUAL, "Spiritual")
    ]

    main_category = MultiSelectField(
        choices=MAIN_CATEGORY
    )

    org_name = models.CharField(max_length=128)
    description = models.TextField(max_length=512)
    street = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, default='Seattle')
    state = USStateField(default='WA')
    zip_code = USZipCodeField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    phone_number = PhoneNumberField()
    tags = TaggableManager(blank=True)
    image = models.ImageField(upload_to='photos', null=True, blank=True)


    def __repr__(self):
        """Print org info."""
        return """
        org_name: {}
        description: {}
        main_category: {}
        address: {} {}, {} {}
        website: {}
        phone_number: {}
        tags: {}
        """.format(self.org_name,
                   self.description,
                   self.main_category,
                   self.street,
                   self.city,
                   self.state,
                   self.zip_code,
                   self.website,
                   self.phone_number,
                   [name for name in self.tags.names()])


    def __str__(self):
        """Print organization information."""
        return self.__repr__()

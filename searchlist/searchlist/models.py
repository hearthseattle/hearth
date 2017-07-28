"""Model for search profiles."""


from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from taggit.managers import TaggableManager
from localflavor.us.models import (
    USStateField,
    USZipCodeField,
    PhoneNumberField
)


MAIN_CATEGORY = [
    ("Crisis", "Crisis"),
    ("Addiction", "Addiction"),
    ("Childcare", "Childcare"),
    ("Youth Services", "Youth Services"),
    ("Veteran", "Veteran"),
    ("Rehabilitation", "Rehabilitation"),
    ("Mental/Physical Disability", "Mental/Physical Disability"),
    ("Education", "Education"),
    ("Employment", "Employment"),
    ("Finances", "Finances"),
    ("Clothing/Housewares", "Clothing/Housewares"),
    ("Food", "Food"),
    ("Healthcare", "Healthcare"),
    ("Shelter", "Shelter"),
    ("Legal", "Legal"),
    ("Identification", "Identification"),
    ("Spiritual", "Spiritual")
]


@python_2_unicode_compatible
class Resource(models.Model):
    """Model for the organization."""

    main_category = models.CharField(
        max_length=25,
        choices=MAIN_CATEGORY
    )

    org_name = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    street = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, default='Seattle')
    state = USStateField(default='Washington')
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
        """.format(self.org_name,
                   self.description,
                   self.main_category,
                   self.street,
                   self.city,
                   self.state,
                   self.zip_code,
                   self.website,
                   self.phone_number)

    def __str__(self):
        """Print organization information."""
        return self.__repr__()

"""Model for search profiles."""


from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from taggit.managers import TaggableManager
from django.core.validators import RegexValidator


MAIN_CATEGORY = (
    ("shelter", "shelter"),
    ("food", "food"),
    ("clinic", "clinic")
)

RATINGS = (
    ("one badge", "one badge"),
    ("two badge", "two badge"),
    ("three badge", "three badge")
)

AGE_RANGE = (
    ("<=17", "<=17"),
    ("18-25", "18-25"),
    (">26", ">26")
)


@python_2_unicode_compatible
class Resource(models.Model):
    """Model for the organization."""

    main_category = models.CharField(
        max_length=25,
        choices=MAIN_CATEGORY
    )

    ratings = models.CharField(
        max_length=25,
        choices=RATINGS,
        default="one badge",
        blank=True,
        null=True
    )

    age_range = models.CharField(
        max_length=25,
        choices=AGE_RANGE,
        blank=True,
        null=True
    )

    org_name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=400, default='')
    location = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(max_length=20, validators=[phone_regex], blank=True)
    tags = TaggableManager(blank=True)

    def __repr__(self):
        """Print org info."""
        return """
        org_name: {}
        description: {}
        main_category: {}
        age_range: {}
        ratings: {}
        location: {}
        website: {}
        phone_number: {}
        """.format(self.org_name, self.description, self.main_category, self.age_range, self.ratings, self.location, self.website, self.phone_number)

    def __str__(self):
        """Print organization information."""
        return self.__repr__()

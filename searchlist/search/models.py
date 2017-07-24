"""Model for search profiles."""


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from taggit.managers import TaggableManager


MAIN_CATEGORY = (
    ("center", "center"),
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


class ProfileManager(models.Manager):
    """Manage search profiles."""

    def get_queryset(self):
        """Return all active searches."""
        return super(ProfileManager, self).get_queryset().filter(user__is_active=True).all()


@python_2_unicode_compatible
class SearchProfile(models.Model):
    """A profile for organization in our application."""

    org = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )
    main_category = models.CharField(
        max_length=25,
        choices=MAIN_CATEGORY,
        default="center",
        null=True
    )
    ratings = models.CharField(
        max_length=25,
        choices=RATINGS,
        default="one badge",
        null=True
    )

    age_range = models.CharField(
        max_length=25,
        choices=AGE_RANGE,
        null=True
    )

    location = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    objects = models.Manager()
    active = ProfileManager()
    tags = TaggableManager()

    @property
    def is_active(self):
        """Active status."""
        return self.user.is_active

    def __repr__(self):
        """Print username."""
        return """
        org_name: {}
        main_category: {}
        ratings: {}
        location: {}
        website: {}
        """.format(self.org.username, self.main_category, self.age_range, self.ratings, self.location, self.website)

    def __str__(self):
        """Print organization name."""
        return self.__repr__()


@receiver(post_save, sender=User)
def make_profile_for_new_org(sender, **kwargs):
    """New Profile instances."""
    if kwargs['created']:
        new_profile = SearchProfile(
            org=kwargs['instance']
        )
        new_profile.save()

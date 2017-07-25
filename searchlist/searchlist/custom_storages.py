"""Custom storage classes for static and media files."""
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    """Custom storage class for static files."""

    location = settings.STATICFILES_LOCATION


class MediaStorage(S3BotoStorage):
    """Custom storage class for media files."""

    location = settings.MEDIAFILES_LOCATION
"""Tests for resource models."""

from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
from models import 
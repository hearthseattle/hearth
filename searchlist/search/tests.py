"""Tests for resource models."""

from django.conf import settings
from django.urls import reverse_lazy
from django.test import TestCase, Client, RequestFactory
from search.models import Resource
from search.views import OrgListView, OrgDetailView
from bs4 import BeautifulSoup
import factory
import faker
import datetime
import os
import random


fake = faker.Faker()

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

HERE = os.path.dirname(__file__)

############ MODEL TESTS
class ResourceFactory(factory.django.DjangoModelFactory):
    """Factory for creating resources."""

    class Meta:
        """Attribute to resource model."""

        model = Resource

    org_name = factory.Sequence(
        lambda n: 'Resource{}'.format(n)
    )
    main_category = random.choice(MAIN_CATEGORY)[0]
    description = fake.text(254)
    ratings = random.choice(RATINGS)[0]
    age_range = random.choice(AGE_RANGE)[0]
    location = fake.address()
    website = fake.domain_name()


class ResourceTestModels(TestCase):
    """Test class for resource models."""

    def setUp(self):
        """Create a resource."""
        resource = ResourceFactory.build()
        resource.save()
        self.resource = resource

    def test_adding_resource_works(self):
        """Test that we successfully add resources."""
        self.assertEqual(Resource.objects.count(), 1)

    def test_no_null_values_for_some(self):
        """Test that we can't put null values for certain fields."""
        pass

    def test_can_change_settings(self):
        """Test that settings can be changed for certain resources."""
        self.resource.age_range = AGE_RANGE[1][0]
        self.resource.ratings = RATINGS[1][0]
        self.resource.main_category = MAIN_CATEGORY[1][0]
        self.assertEqual([self.resource.age_range,
                          self.resource.ratings,
                          self.resource.main_category],
                         ["18-25", "two badge", "shelter"])

    def test_delete_resources(self):
        """Test that delete works."""
        self.assertEqual(Resource.objects.count(), 1)
        resource_two = ResourceFactory.build()
        resource_two.save()
        self.assertEqual(Resource.objects.count(), 2)
        resource_two.delete()
        self.assertEqual(Resource.objects.count(), 1)

    def test_adding_a_bunch_of_resources(self):
        """Test adding a bunch of resources."""
        self.assertEqual(Resource.objects.count(), 1)
        more_resources = [ResourceFactory.build() for i in range(5)]
        for resource in more_resources:
            resource.save()
        self.assertTrue(Resource.objects.count(), 6)


############ VIEW TESTS
class OrgListTestView(TestCase):
    """."""
    def testOrgListValues(self):
        view = OrgListView.as_view()
        request = RequestFactory().get('/fake-path')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "search/org_list.html")
        import pdb; pdb.set_trace()
        self.assertEqual(response.model, Resource)
        self.assertEqual(response.context_object_name, 'orgs')
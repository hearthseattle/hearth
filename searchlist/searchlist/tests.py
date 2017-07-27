"""Tests for views, model and user privileges."""

from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from searchlist.models import Resource
from searchlist.views import CreateResource, EditResource, DeleteResource, HomePageView, ResourceDetailView
from bs4 import BeautifulSoup
import factory
import faker
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
    org_name = fake.name()
    phone_number = factory.Sequence(lambda n: '123-555-%04d' % n)
    tags = ['substance recovery', 'mental health', 'disability', 'food', 'domestic violence', 'service animals']


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

    def test_model_fields(self):
        """Test organization is created with designated fields."""
        test_org = Resource()
        test_org.main_category = 'shelter'
        test_org.org_name = 'test_org'
        test_org.description = 'test case'
        test_org.age_range = '18-25'
        test_org.ratings = 'two badge'
        test_org.location = 'seattle'
        test_org.website = 'http://www.test_org.com'
        test_org.phone_number = '1234567890'
        test_org.tags = 'shelter'
        test_org.save()
        self.assertTrue(test_org.main_category == 'shelter')
        self.assertTrue(test_org.org_name == 'test_org')
        self.assertTrue(test_org.description == 'test case')
        self.assertTrue(test_org.age_range == '18-25')
        self.assertTrue(test_org.ratings == 'two badge')
        self.assertTrue(test_org.location == 'seattle')
        self.assertTrue(test_org.website == 'http://www.test_org.com')
        self.assertTrue(test_org.phone_number == '1234567890')
        self.assertTrue(test_org.tags == 'shelter')

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

    def test_add_resources(self):
        """Test adding a bunch of resources."""
        self.assertEqual(Resource.objects.count(), 1)
        more_resources = [ResourceFactory.build() for i in range(5)]
        for resource in more_resources:
            resource.save()
        self.assertTrue(Resource.objects.count(), 6)


############ ROUTE, TEMPLATE TESTS
class ViewRouteTest(TestCase):
    """."""

    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()

    def test_homepage_view(self):
        """Reverse home route to test link exist."""
        response = self.client.get(reverse_lazy('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searchlist/home.html')

    def test_homepage_has_checkbox(self):
        """Test homepage checkbox exists."""
        response = self.client.get(reverse_lazy('home'))
        self.assertTrue(b'checkbox' in response.content)

    def test_404_view(self):
        """Test not exist resource 404 page appears."""
        response = self.client.get('foo')
        self.assertEqual(response.status_code, 404)
        # self.assertTemplateUsed(response, 'searchlist/404.html')

    def test_createresource_view(self):
        """Test reverse creatersource route to test link exists."""
        response = self.client.get(reverse_lazy('/resource/new/'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searchlist/resource_form.html')

    def test_Editresource_view(self):
        """Test reverse editsource route to test link exists."""
        response = self.client.get(reverse_lazy('/resource/1/edit/'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searchlist/resource_form.html')

    def test_Deleteresource_view(self):
        """Test reverse deletesource route to test link exists."""
        response = self.client.get(reverse_lazy('/resource/1/delete/'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searchlist/delete_resource.html')

    def test_Resourcedetail_view(self):
        """Test reverse resourcedetail route to test link exists."""
        response = self.client.get(reverse_lazy('/resource/1'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searchlist/resource_detail.html')

    def test_Login_view(self):
        """Test reverse login route to test link exists."""
        response = self.client.get(reverse('/login/'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


############ View TESTS

class RegistrationTest(TestCase):
    """."""

    def setUp(self):
        """."""
        self.client = Client()

    def test_valid_user_login(self):
        """Test login process."""
        user = User(username='fred', email='test@test.com')
        user.set_password('temporary')
        user.save()
        self.client.login(username='fred', password='temporary')
        response = self.client.get('/login/', follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_invalid_user_login_username(self):
        """Test login process."""
        user = User(username='fred', email='test@test.com')
        user.set_password('temporary')
        user.save()
        self.client.login(username='bill', password='temporary')
        response = self.client.get('/login/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_valid_user_logout(self):
        """Test logout process."""
        user = User(username='fred', email='test@test.com')
        user.set_password('temporary')
        user.save()
        self.client.login(username='fred', password='temporary')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)


# class CreateResourceTest(TestCase):
#     """Create a resource."""

#     def setUp(self):
#         """."""
#         self.client = Client()

#     def test_CreateResourceView()


class DeleteResourceTest(TestCase):
    """Delete a resource."""

    def setUp(self):
        """Create a resource."""
        self.client = Client()
        self.resource = ResourceFactory.build()
        self.resource.save()

    def test_Deleteresource_cancel_button(self):
        """Test cancel button."""
        self.assertEqual(Resource.objects.count(), 1)
        idx = self.resource.id
        response = self.client.get('/resource/{}/delete/'.format(idx))
        html = BeautifulSoup(response.content, 'Cancel')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Resource.objects.count(), 1)

    def test_Deleteresource_confirm_button(self):
        """Test confirm button."""
        self.assertEqual(Resource.objects.count(), 1)
        idx = self.resource.id
        self.client.post('/resource/{}/delete/'.format(idx))
        self.assertEqual(Resource.objects.count(), 0)
        self.assertEqual(response.status_code, 302)

    # class EditResourceTest(TestCase):
    # """Edit a resource."""

    # def setUp(self):
    #     """."""
    #     self.client = Client()

    # def test_edit


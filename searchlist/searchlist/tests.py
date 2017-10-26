"""Tests for views, model and user privileges."""
from bs4 import BeautifulSoup as soup
from django.contrib.auth.models import User
from django.test import (
    TestCase,
    Client,
    RequestFactory
)
from django.urls import reverse_lazy
from searchlist.models import Resource
import factory
import faker
import os
import random


fake = faker.Faker()

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
    services = random.choice(MAIN_CATEGORY)[0]
    description = fake.text(100)
    website = fake.domain_name()
    phone_number = factory.Sequence(lambda n: '123-555-%04d' % n)
    tags = random.choice(['substance recovery', 'mental health', 'disability', 'food',
                          'domestic violence', 'service animals'])


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
        test_org.services = 'Addiction'
        test_org.org_name = 'test_org'
        test_org.description = 'test case'
        test_org.website = 'http://www.test_org.com'
        test_org.phone_number = '1234567890'
        test_org.tags = 'Addiction'
        test_org.save()
        self.assertTrue(test_org.services == 'Addiction')
        self.assertTrue(test_org.org_name == 'test_org')
        self.assertTrue(test_org.description == 'test case')
        self.assertTrue(test_org.website == 'http://www.test_org.com')
        self.assertTrue(test_org.phone_number == '1234567890')
        self.assertTrue(test_org.tags == 'Addiction')

    def test_can_change_settings(self):
        """Test that settings can be changed for certain resources."""
        self.resource.services = MAIN_CATEGORY[1][0]
        self.assertEqual(self.resource.services, "Addiction")

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


# ############ ROUTE, TEMPLATE TESTS
class ViewRouteTest(TestCase):
    """Test for the various views."""

    def setUp(self):
        """Set up for view tests."""
        self.client = Client()
        self.request = RequestFactory()
        self.resource = ResourceFactory.build()
        self.resource.save()

        test_fred = User()
        test_fred.username = 'fred'
        test_fred.set_password('temporary')
        test_fred.save()

    def test_homepage_view(self):
        """Reverse home route to test link exist."""
        response = self.client.get(reverse_lazy('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searchlist/home.html')

    def test_homepage_has_checkbox(self):
        """Test homepage checkbox exists."""
        response = self.client.get(reverse_lazy('home'))
        self.assertTrue(b'checkbox' in response.content)

    def test_create_resource_view_returns_status_200(self):
        """Test create resource page returns status code 200."""
        self.client.login(username='fred', password='temporary')
        response = self.client.get('/resource/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searchlist/resource_form.html')

    def test_edit_resource_view_returns_status_code_200(self):
        """Test  edit resource page returns status code 200."""
        self.client.login(username='fred', password='temporary')
        idx = self.resource.id
        response = self.client.get("/resource/{}/edit/".format(idx))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searchlist/resource_form.html')

    def test_delete_resource_view_returns_status_code_200(self):
        """Test reverse delete source route to test link exists."""
        self.client.login(username='fred', password='temporary')
        idx = self.resource.id
        response = self.client.get('/resource/{}/delete/'.format(idx))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searchlist/delete_resource.html')

    # def test_resource_detail_view_with_correct_id_returns_status_200(self):
    #     """Test resource detail view functions correctly."""
    #     idx = self.resource.id
    #     response = self.client.get('/resource/{}'.format(idx))
    #     import pdb; pdb.set_trace()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'searchlist/resource_detail.html')

    def test_bad_detail_view_returns_404(self):
        """Test non existent resource returns 404."""
        response = self.client.get('/resource/200')
        self.assertEqual(response.status_code, 404)

    def test_login_view_returns_status_code_200(self):
        """Test reverse login route to test link exists."""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


# ############ View TESTS

class RegistrationCreateEditDeleteResourceTest(TestCase):
    """."""

    def setUp(self):
        """Set up for resource tests."""
        self.client = Client()
        test_fred = User()
        test_fred.username = 'fred'
        test_fred.set_password('temporary')
        test_fred.save()
        self.resource = ResourceFactory.build()
        self.resource.save()

    def test_valid_user_login(self):
        """Test login process with good crendentials."""
        self.client.login(username='fred', password='temporary')
        response = self.client.get('/login/', follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_invalid_user_login_username(self):
        """Test login process with bad credentials."""
        self.client.login(username='bill', password='temporary')
        response = self.client.get('/login/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_valid_user_logout(self):
        """Test logout process."""
        self.client.login(username='fred', password='temporary')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_delete_resource_shows_cancel_button(self):
            """Test cancel button shows on delete resource page."""
            self.client.login(username='fred', password='temporary')
            self.assertEqual(Resource.objects.count(), 1)
            idx = self.resource.id
            response = self.client.get(reverse_lazy('delete', kwargs={'pk': idx}))
            html = soup(response.content, 'html.parser')
            cancel = html.findAll('a', {'href': "/resource/1/edit/"})
            self.assertTrue(cancel)

    # def test_homepage_view_links_to_a_single_resource(self):
    #     """Test homepage resource list total."""
    #     response = self.client.get(reverse_lazy('home'))
    #     html = soup(response.content, "html.parser")
    #     link = html.findAll("a", {"href": "/resource/"})
    #     # import pdb; pdb.set_trace()
    #     self.assertTrue(link)

    ##### CSS Element Tests
    def test_template_used_for_home_html_is_base(self):
        """Test that template used for home.html is the base.html."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'searchlist/base.html')

    def test_template_not_used_for_home_html(self):
        """Test that template used for home.html is not 404.html."""
        response = self.client.get('/')
        self.assertTemplateNotUsed(response, '404.html')

    def test_template_not_used_for_delete_resource_html(self):
        """Test that template used for delete_resource.html is not base.html."""
        response = self.client.get('/delete')
        self.assertTemplateNotUsed(response, 'base.html')

    def test_template_not_used_for_resource_detail_html(self):
        """Test that template used for resource_detail.html is not base.html."""
        response = self.client.get('/delete')
        self.assertTemplateNotUsed(response, 'base.html')

    def test_template_not_used_for_resource_form_html(self):
        """Test that template used for resource_form.html is not base.html."""
        response = self.client.get('/resource_detail')
        self.assertTemplateNotUsed(response, 'base.html')

    def test_home_contains_checkbox(self):
        """Test that there is checkboxes on the home page."""
        response = self.client.get('/')
        html = soup(response.content, "html.parser")
        link = html.findAll("div", {"class": "checkbox"})
        self.assertTrue(link)

    def test_home_contains_contact_info_section(self):
        """Testing contact info appears."""
        response = self.client.get('/')
        html = soup(response.content, "html.parser")
        link = html.findAll("section", {"id": "contact"})
        self.assertTrue(link)

    def test_home_contains_link_to_email(self):
        """Test that the email link works in home page."""
        response = self.client.get('/')
        html = soup(response.content, "html.parser")
        link = html.findAll("a", {"href": "mailto:admin@hearthseattle.org"})
        self.assertTrue(link)

    def test_home_contains_contact_in_navbar(self):
        """Test that the nav bar contains a contact button."""
        response = self.client.get('/')
        html = soup(response.content, "html.parser")
        link = html.findAll("a", {"href": "#contact"})
        self.assertTrue(link)

    # def test_homepage_view_has_links_to_multiple_resources(self):
    #     """Test homepage resource list total."""
    #     ResourceFactory.build()
    #     ResourceFactory.build()
    #     response = self.client.get(reverse_lazy('home'))
    #     html = soup(response.content, "html.parser")
    #     link = html.findAll("a", {"href": "/resource/*"})
    #     print(len(link))
    #     self.assertTrue(len(link) == 3)

#     def test_homepageview_checkbox(self):
#         """Test homepage."""
#         response = self.client.get(reverse_lazy('home'))
#         assert checkbox selection is save
#
#     def test_homepageview_filtercontent(self):
#         """Test homepage."""
#         response = self.client.get(reverse_lazy('home'))
#         assert filter content displays per selected criteria
#
#
#
#     def test_deleteresource_confirm_button(self):
#         """Test confirm button."""
#         self.assertEqual(Resource.objects.count(), 1)
#         idx = self.resource.id
#         self.client.post('/resource/{}/delete/'.format(idx))
#         self.assertEqual(Resource.objects.count(), 0)
#         self.assertEqual(response.status_code, 302)
#         test html success_message
#
#     def test_createresource(self):
#         """Test adding resource."""
#         self.assertEqual(Resource.objects.count(), 1)
#         add resource:fields = ['services', 'org_name',
#               'description', 'street', 'city', 'state', 'zip_code', 'website',
#               'phone_number', 'tags']
#         resource.object.save()
#         success_url = reverse_lazy('home')
#         self.assertEqual(Resource.objects.count(), 2)
#
#     def test_updateresource(self):
#         """Test updating resource."""
#         current resource = etc.
#         change some fields = ['services', 'org_name',
#               'description', 'street', 'city', 'state', 'zip_code', 'website',
#               'phone_number', 'tags']
#         resource.oject.save()
#         current resource = changed fields
#         success_url = reverse_lazy('home')
#
#
# class DetailResourceTest(TestCase):
#     """Test google map api."""
#
#     def setUp(self):
#         """."""
#         self.key = ''
#         self.client = googlemaps.Client(self.key)
#         self.location = (lat, long )
#         self.type = 'shelter'
#         self.language = 'en-ENG'
#         self.radius = 10
#
# @responses.activate
#     def test_places_text_search(self):
#         url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
#         responses.add(responses.GET, url,
#                       body='{"status": "OK", "results": [], "html_attributions": []}',
#                       status=200, content_type='application/json')
#
#         self.client.places('restaurant', location=self.location,
#                            radius=self.radius, language=self.language,
#                            min_price=1, max_price=4, open_now=True,
#                            type=self.type)
#
#         self.assertEqual(1, len(responses.calls))
#         self.assertURLEqual('%s?language=en-AU&location=-33.86746%%2C151.20709&'
#                             'maxprice=4&minprice=1&opennow=true&query=restaurant&'
#                             'radius=100&type=shelter&key=%s'
#                             % (url, self.key), responses.calls[0].request.url)
#
#     def test_detailresource_edit_button(self):
#         """Test edit button."""
#         idx = self.resource.id
#         response = self.client.get('/resource/{}/delete/'.format(idx))
#         html = BeautifulSoup(response.content, 'Edit')
#         self.assertEqual(response.status_code, 302) #redirect to edit page

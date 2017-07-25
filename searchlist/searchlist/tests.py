from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy


# class HomePageTests(TestCase):
#     """Test the content of the homepage."""

#     def setUp(self):
#         """Setup."""
#         self.client = Client()

#     def test_home_ok(self):
#         """Test that home page is available to logged out user."""
#         resp = self.client.get(reverse_lazy('home'))
#         self.assertEqual(resp.status_code, 200)

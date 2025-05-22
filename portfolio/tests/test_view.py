from django.test import TestCase, Client
from django.urls import reverse
from portfolio.models import *

class HomeViewTest(TestCase):
    """Test suite for the home page view functionality.
    Verifies both the response status and template usage."""
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        
    def _get_home_response(self):
        """Helper method to get response from home page."""
        return self.client.get(self.url)
    
    def test_should_return_success_status(self):
        response = self._get_home_response()
        self.assertEquals(response.status_code, 200)
        
    def test_should_use_correct_template(self):
        response = self._get_home_response()
        self.assertTemplateUsed(response, 'home.html')


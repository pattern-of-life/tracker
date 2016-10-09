from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
import re


class HomePageTestCase(TestCase):
    """Create Home Page test case."""

    def setUp(self):
        """Set up response for home page test case."""
        self.response = self.client.get(reverse("homepage"))

    def test_home_page_uses_right_template(self):
        """Assert home page view renders our view."""
        for template_name in [
            'tracker/home.html',
            'tracker/base.html'
        ]:
            self.assertTemplateUsed(self.response, template_name)

    def test_home_page_welcome_message(self):
        """Assert welcome message shows on home page."""
        self.assertContains(self.response, "Welcome to TrackerPy")

class RegistrationTestCase(TestCase):
    """Set up registration test case."""
    def setUp(self):
        """Set up response for registration test case."""
        self.response = self.client.post('/accounts/register/', {
            'username': 'derek',
            'email': 'derek@derek.com',
            'password1': 'IamDerek#&$hearMeRoar',
            'password2': 'IamDerek#&$hearMeRoar'
        })

    def test_client_response_code(self):
        """Test 302 response code received."""
        self.assertEqual(self.response.status_code, 302)

    def test_client_response_content(self):
        """Test content received upon successful registration."""
        self.assertEqual(self.response.url, "/accounts/register/complete/")

    def test_registration_complete_page_uses_right_template(self):
        """Assert that registration page view is rendered with our template."""
        for template_name in [
            "registration/activation_email_subject.txt",
            "registration/activation_email.txt"
        ]:
            self.assertTemplateUsed(self.response, template_name)

    def test_email_activation_works(self):
        """Test user is activated by email."""
        user = User.objects.first()
        self.assertFalse(user.is_active)
        find_url = r"\/accounts\/activate\/.*"
        activation_url = re.findall(find_url, mail.outbox[0].body)[0]
        self.client.get(activation_url)
        self.assertTrue(User.objects.first().is_active)

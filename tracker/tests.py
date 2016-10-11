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
        user = User(username="test")
        user.save()
        self.client.force_login(user)
        self.auth_response = self.client.get(reverse("homepage"))

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

    def test_login_displayed(self):
        """Assert link to login on home page."""
        self.assertContains(self.response, reverse('auth_login'))

    def test_sign_up_displayed(self):
        """Assert link to login on home page."""
        self.assertContains(self.response, reverse('registration_register'))

    def test_sign_out_not_displayed(self):
        """Assert link to login on home page."""
        self.assertNotContains(self.response, reverse('auth_logout'))

    def test_authenticated_user_log_in_not_displayed(self):
        """Assert authenticated user can't see login link."""
        self.assertNotContains(self.auth_response, reverse('auth_login'))

    def test_authenticated_user_sign_up_not_displayed(self):
        """Assert authenticated user can't see sign up link."""
        url = reverse('registration_register')
        self.assertNotContains(self.auth_response, url)

    def test_authenticated_user_log_out_displayed(self):
        """Assert authenticated user can see log out link."""
        self.assertContains(self.auth_response, reverse('auth_logout'))


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


class LoginTestCase(TestCase):
    """Test case for login and logout."""

    def setUp(self):
        """Create a user to log in with."""
        self.username = 'foo'
        self.password = 'somethingsomething'
        self.user = User(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def test_login_authenticates(self):
        """Test POSTing to login."""
        self.assertNotIn('_auth_user_id', self.client.session.keys())
        response = self.client.post(reverse('auth_login'), dict(
            username=self.username,
            password=self.password
        ))
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session.keys())

    def test_logout(self):
        """Test GETing logout"""
        self.client.force_login(self.user)
        self.assertIn('_auth_user_id', self.client.session.keys())
        response = self.client.get(reverse('auth_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session.keys())


class AboutTestCase(TestCase):
    """Test case for about view."""

    def setUp(self):
        """Set up response to go to about page."""
        self.response = self.client.get(reverse("aboutpage"))

    def test_about_page_uses_right_template(self):
        """Assert about page view renders our view."""
        for template_name in [
            'tracker/about.html',
            'tracker/base.html'
        ]:
            self.assertTemplateUsed(self.response, template_name)

    def test_about_page_message(self):
        """Assert about titles show on about page."""
        self.assertContains(self.response, "About The Team")

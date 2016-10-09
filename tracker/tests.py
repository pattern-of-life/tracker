from django.test import TestCase
from django.urls import reverse


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

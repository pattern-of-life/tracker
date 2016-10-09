from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TrackerProfileTestCase(TestCase):
    """Create test class for TrackerProfile model."""

    def setUp(self):
        """Set up a fake user and profile."""
        self.user = User(username='test')
        self.user.set_password('test')
        self.user.save()

    def test_user_exists(self):
        """Test the user exists."""
        self.assertTrue(self.user is not None)

    def test_username(self):
        """Test the username is correct."""
        self.assertEqual(self.user.username, 'test', 'wrong username')

    def test_profile_exists(self):
        """Test that the user has a profile."""
        self.assertTrue(self.user.profile is not None)

    def test_profile_attached_to_right_user(self):
        """Test profile is attached to right user."""
        self.assertEqual(self.user.profile.user.username, 'test')


class TrackerProfileViewTestCase(TestCase):
    """Test view for tracker profile view."""

    def setUp(self):
        """Set up fake user and log in."""
        self.username = "test"
        self.user = User(username=self.username)
        self.user.save()
        self.biography = "biography"
        self.user.profile.bio = self.biography
        self.user.profile.save()
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('profile'))

    def test_profile_status_code(self):
        """Test status code for authenticated user."""
        self.assertTrue(self.response.status_code, 200)

    def test_profile_shows_username(self):
        """Test status code for authenticated user."""
        self.assertContains(self.response, self.username)

    def test_profile_shows_biography(self):
        """Test status code for authenticated user."""
        self.assertContains(self.response, self.biography)

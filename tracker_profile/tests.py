from django.test import TestCase
from django.contrib.auth.models import User


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

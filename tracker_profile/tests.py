from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from tracker_device.models import TrackerDevice


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
        self.device = TrackerDevice(user=self.user)
        self.device.save()
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

    def test_device_detail_link(self):
        """Test that provfile view renders device detail view links."""
        url = reverse('detail_device', args=[self.device.pk])
        self.assertContains(self.response, url)


class TrackerProfileEditViewTestCase(TestCase):
    """Test profile editing."""

    def setUp(self):
        """Create a user to edit."""
        self.username = "test"
        self.user = User(username=self.username)
        self.user.save()
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('edit_profile'))

    def test_edit_profile_status_code(self):
        """Test status code of edit profile view is 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_edit_profile_bio(self):
        """Test status code of edit profile view is 200."""
        expected_bio = 'foo'
        data = dict(bio=expected_bio)
        response = self.client.post(reverse('edit_profile'), data)
        self.assertEqual(response.status_code, 302)
        actual_bio = User.objects.first().profile.bio
        self.assertEqual(actual_bio, expected_bio)

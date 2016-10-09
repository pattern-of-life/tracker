from django.test import TestCase
from django.contrib.auth.models import User
from .models import TrackerDevice


class TrackerDeviceTest(TestCase):
    """Create test class for tracker device model."""
    def setUp(self):
        """Set up fake user and device."""
        self.user = User(username='test')
        self.user.save()
        self.device = TrackerDevice(user=self.user)
        self.device.save()

    def test_device_exists(self):
        """Test the user has a device."""
        self.assertEqual(self.user.devices.count(), 1)

    def test_device_attached_to_right_user(self):
        """Test the device is attached to the right user."""
        self.assertEqual(self.device.user.username, 'test')

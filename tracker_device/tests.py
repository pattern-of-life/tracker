from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .models import TrackerDevice, DataPoint, Route
from django.utils import timezone


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


class DataPointTestCase(TestCase):
    """Test case for data point model."""

    def setUp(self):
        """Set up device to associate data points with."""
        self.user = User(username='test')
        self.user.save()
        self.device = TrackerDevice(user=self.user)
        self.device.save()
        self.data_count = 5
        for i in range(self.data_count):
            DataPoint(
                device=self.device,
                lat=i,
                lng=i,
                elevation=i,
                time=timezone.now()
            ).save()

    def test_data_point(self):
        """Test data points exist."""
        self.assertEqual(self.device.data.count(), self.data_count)

    def test_data_attached_to_right_device(self):
        """Test the data is attached to the right device."""
        self.assertEqual(self.device.data.first().device.user.username, 'test')


class RouteTestCase(TestCase):
    """Test case for route model."""

    def setUp(self):
        """Set up some data points and a route."""
        self.user = User(username='test')
        self.user.save()
        self.device = TrackerDevice(user=self.user)
        self.device.save()
        Route(
            name='a route',
            start=timezone.now(),
            device=self.device
        ).save()

    def test_route_exists(self):
        """Check route exists."""
        self.assertEqual(self.device.routes.count(), 1)

    def test_route_attached_to_device(self):
        """Check route exists."""
        self.assertEqual(self.device.routes.first().name, 'a route')


class CreateDeviceViewTestCase(TestCase):
    """Test case for creating a new device."""

    def setUp(self):
        """Set up a user to make a device with."""
        self.user = User(username="test")
        self.user.save()
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('create_device'))

    def test_create_device_status_code(self):
        """Check status code for device create view."""
        self.assertEqual(self.response.status_code, 200)

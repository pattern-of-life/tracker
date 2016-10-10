from uuid import uuid4
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from tracker_device.models import TrackerDevice, DataPoint, Route


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

    def test_creating_new_device(self):
        """Check status code for device create view."""
        self.assertEqual(TrackerDevice.objects.count(), 0)
        data = dict(mode='quiet')
        response = self.client.post(reverse('create_device'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TrackerDevice.objects.count(), 1)


class EditDeviceViewTestCase(TestCase):
    """Test case for editing existing devices."""

    def setUp(self):
        """Set up a user and device to be edited."""
        user = User(username='carrie')
        user.save()
        self.client.force_login(user)
        self.device = TrackerDevice(user=user, id_uuid=uuid4())
        self.device.save()

    def test_edit_view_status_code(self):
        """Test status code of edit device page."""
        pk = self.device.pk
        response = self.client.get(reverse('edit_device', args=[pk]))
        self.assertEqual(response.status_code, 200)

    def test_edit_view_post(self):
        """Test posting to edit view updates model."""
        pk = self.device.pk
        mode = 'debug'
        data = dict(mode=mode)
        response = self.client.post(reverse('edit_device', args=[pk]), data)
        self.assertEqual(response.status_code, 302)
        device = TrackerDevice.objects.first()
        self.assertEqual(device.mode, mode)

    def test_edit_view_by_other_user(self):
        """Test posting to edit view returns error when not owner of device."""
        new_user = User(username='lowell')
        new_user.save()
        self.client.force_login(new_user)
        data = dict(title='bad', mode='debug')
        self.client.post(reverse('edit_device', args=[self.device.pk]), data)
        device = TrackerDevice.objects.first()
        self.assertNotEqual(device.title, 'bad')


class DeleteDeviceViewTestCase(TestCase):
    """Test case for deleting devices."""

    def setUp(self):
        """Set up a user and device to be deleted."""
        user = User(username='derek')
        user.save()
        self.client.force_login(user)
        self.device = TrackerDevice(user=user, id_uuid=uuid4())
        self.device.save()

    def test_delete_view_post_status_code(self):
        """Test 302 status code when post to delete view."""
        response = self.client.post(reverse('delete_device', args=[self.device.pk]))
        self.assertEqual(response.status_code, 302)

    def test_delete_view_get_status_code(self):
        """Test 200 status code when get to delete view."""
        response = self.client.get(reverse('delete_device', args=[self.device.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_view_no_device_in_db(self):
        """Test no device in database after delete."""
        self.client.post(reverse('delete_device', args=[self.device.pk]))
        total_devices = TrackerDevice.objects.count()
        self.assertEqual(total_devices, 0)

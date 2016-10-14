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

    def test_unauthenticated_user_get_view(self):
        """Check unauthenticated user is redirected."""
        self.client.logout()
        response = self.client.get(reverse('create_device'))
        url = reverse('auth_login') + '?next=' + reverse('create_device')
        self.assertRedirects(response, url)

    def test_unauthenticated_user_post_view(self):
        """Check unauthenticated user is redirected on post."""
        self.client.logout()
        data = dict(mode='quiet')
        response = self.client.post(reverse('create_device'), data)
        url = reverse('auth_login') + '?next=' + reverse('create_device')
        self.assertRedirects(response, url)
        self.assertEqual(TrackerDevice.objects.count(), 0)


class EditDeviceViewTestCase(TestCase):
    """Test case for editing existing devices."""

    def setUp(self):
        """Set up a user and device to be edited."""
        user = User(username='carrie')
        user.save()
        self.client.force_login(user)
        self.device = TrackerDevice(user=user)
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
        self.user2 = User(username='fred')
        self.user2.save()
        self.client.force_login(user)
        self.device = TrackerDevice(user=user)
        self.device.save()
        self.url = reverse('delete_device', args=[self.device.pk])

    def test_delete_view_post_status_code(self):
        """Test 302 status code when post to delete view."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_view_get_status_code(self):
        """Test 200 status code when get to delete view."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_delete_view_no_device_in_db(self):
        """Test no device in database after delete."""
        self.client.post(self.url)
        total_devices = TrackerDevice.objects.count()
        self.assertEqual(total_devices, 0)

    def test_delete_view_unauth_user_redirects(self):
        """Test unauthorized user redirected to login."""
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_view_unauth_user_cannot_delete(self):
        """Test unauthorized user cannot delete device."""
        self.client.logout()
        self.client.post(self.url)
        total_devices = TrackerDevice.objects.count()
        self.assertEqual(total_devices, 1)

    def test_delete_view_wrong_auth_user_redirects(self):
        """Test unauthorized user redirected to login."""
        self.client.force_login(self.user2)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_delete_view_wrong_auth_user_cannot_delete(self):
        """Test unauthorized user cannot delete device."""
        self.client.force_login(self.user2)
        self.client.post(self.url)
        total_devices = TrackerDevice.objects.count()
        self.assertEqual(total_devices, 1)


class CreateRouteViewTestCase(TestCase):
    """Test case for creating routes."""

    def setUp(self):
        """create a user and device to set routes on."""
        user = User(username='derek')
        user.save()
        self.user2 = User(username='fred')
        self.user2.save()
        self.client.force_login(user)
        self.device = TrackerDevice(user=user)
        self.device.save()

    def test_create_route_status_code(self):
        """Test status code is 200 for new route creation."""
        response = self.client.get(reverse('create_route'))
        self.assertEqual(response.status_code, 200)

    def test_create_route_post_status_code(self):
        """Test status code after post is 302."""
        data = {
            "start": "10/21/2016",
            "device": self.device.pk
        }
        response = self.client.post(reverse('create_route'), data)
        self.assertEqual(response.status_code, 302)

    def test_create_route_unauth_user(self):
        """Test unauthorized user cannot create routes."""
        self.client.logout()
        data = {
            "start": "10/21/2016",
            "device": self.device.pk
        }
        response = self.client.post(reverse('create_route'), data)
        self.assertEqual(response.status_code, 302)

    def test_create_route_unauth_user_no_route_in_db(self):
        """Test unauthorized user cannot create a route."""
        self.client.logout()
        data = {
            "start": "10/21/2016",
            "device": self.device.pk
        }
        self.client.post(reverse('create_route'), data)
        total_routes = Route.objects.count()
        self.assertEqual(total_routes, 0)

    def test_create_route_wrong_user(self):
        """Test wrong authorized user cannot create route for other user."""
        self.client.force_login(self.user2)
        data = {
            "start": "10/21/2016",
            "device": self.device.pk
        }
        response = self.client.post(reverse('create_route'), data)
        self.assertEqual(response.status_code, 403)

    def test_create_route_wrong_user_no_route_in_db(self):
        """Test wrong authorized user cannot create a route."""
        self.client.force_login(self.user2)
        data = {
            "start": "10/21/2016",
            "device": self.device.pk
        }
        self.client.post(reverse('create_route'), data)
        total_routes = Route.objects.count()
        self.assertEqual(total_routes, 0)


class EditRouteViewTestCase(TestCase):
    """Test editing a route."""

    def setUp(self):
        """Set up a user, a device, and route to edit."""
        self.user = User(username='hello')
        self.user.save()
        self.other_user = User(username='badguy')
        self.other_user.save()
        self.client.force_login(self.user)
        self.device = TrackerDevice(user=self.user)
        self.device.save()
        self.route = Route(device=self.device, start=timezone.now())
        self.route.save()
        self.url = reverse('edit_route', args=[self.route.pk])

    def test_route_edit_view_status_code(self):
        """Test status code of edit view."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_route_edit_view_post(self):
        """Test status code of edit view."""
        data = {'name': 'new name'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

    def test_route_edit_view_post_changes_route(self):
        """Test posting to edit view changes route."""
        data = {'name': 'new name'}
        self.client.post(self.url, data)
        self.assertEqual(Route.objects.first().name, 'new name')

    def test_route_edit_unauth_status_code(self):
        """Test status code of editing route unauthenticated."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_route_edit_unauth_route_unchanged_in_db(self):
        """Test editing route unauthenticated doesn't change route."""
        self.client.logout()
        bad_name = 'bad name'
        data = {'name': bad_name}
        self.client.post(self.url, data)
        route = Route.objects.first()
        self.assertNotEqual(route.name, bad_name)

    def test_route_edit_wrong_user_status_code(self):
        """Test editing other user's route redirects."""
        self.client.force_login(self.other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_route_edit_wrong_user_route_unchanged_in_db(self):
        """Test editing other user's route doesn't change route."""
        self.client.force_login(self.other_user)
        bad_name = 'bad name'
        data = {'name': bad_name}
        self.client.post(self.url, data)
        route = Route.objects.first()
        self.assertNotEqual(route.name, bad_name)


class DeleteRouteViewTestCase(TestCase):
    """Test case for view for deleting routes."""

    def setUp(self):
        """Set up a user, device, and route to be deleted."""
        self.user = User(username='whoever')
        self.user.save()
        self.other_user = User(username='badguy')
        self.other_user.save()
        self.client.force_login(self.user)
        self.device = TrackerDevice(user=self.user)
        self.device.save()
        self.route = Route(device=self.device, start=timezone.now())
        self.route.save()
        self.url = reverse('delete_route', args=[self.route.pk])

    def test_delete_view_status_code(self):
        """Test delete view status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_delete_view_post_redirects(self):
        """Test delete view status code."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_view_post_deletes_route(self):
        """Test delete view status code."""
        self.assertEqual(Route.objects.count(), 1)
        self.client.post(self.url)
        self.assertEqual(Route.objects.count(), 0)

    def test_delete_route_unauth_status_code(self):
        """Test unauthenticated user redirects to login."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_route_unauth_post_redirects(self):
        """Test unauthenticated user posting to delete view redirects."""
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_route_wrong_user_cannot_delete(self):
        """Test unauthenticated user can't delete a route."""
        self.client.force_login(self.other_user)
        self.assertEqual(Route.objects.count(), 1)
        self.client.post(self.url)
        self.assertEqual(Route.objects.count(), 1)


class CreateDataPointViewTestCase(TestCase):
    """Test view for creating data points."""

    def setUp(self):
        """Set up a device to create data points onto."""
        user = User(username='???')
        user.save()
        self.device = TrackerDevice(user=user)
        self.device.save()

    def test_data_point_status_code(self):
        """Test data point view status code."""
        response = self.client.get(reverse('create_data_point'))
        self.assertEqual(response.status_code, 200)

    def test_data_point_post_creates_point(self):
        """Test data point view status code."""
        self.assertEqual(DataPoint.objects.count(), 0)
        data = dict(
            time='10/10/10',
            lat=323.0,
            lng=232.0,
            elevation=15.3,
            uuid=self.device.id_uuid
        )
        response = self.client.post(reverse('create_data_point'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DataPoint.objects.count(), 1)

    def test_data_point_post_invalid_uuid(self):
        """Check posting to the create data point view with invalid UUID."""
        data = dict(
            time='10/10/10',
            lat=323.0,
            lng=232.0,
            elevation=15.3,
            uuid=';-)'
        )
        response = self.client.post(reverse('create_data_point'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DataPoint.objects.count(), 0)

    def test_data_point_post_incorrect_uuid(self):
        """Check posting to the create data point view with incorrect UUID."""
        data = dict(
            time='10/10/10',
            lat=323.0,
            lng=232.0,
            elevation=15.3,
            uuid=uuid4()
        )
        response = self.client.post(reverse('create_data_point'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DataPoint.objects.count(), 0)

    def test_create_data_point_unauthenticated(self):
        """Test data point redirects to home page."""
        data = dict(
            time='10/10/10',
            lat=323.0,
            lng=232.0,
            elevation=15.3,
            uuid=self.device.id_uuid
        )
        url = reverse('create_data_point')
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, reverse('homepage'))


class TestDetailDeviceView(TestCase):
    """Tests for detail device view."""

    TEST_DATA = map(timezone.make_aware, [
        timezone.datetime(1974, 5, 17, 0, 0),
        timezone.datetime(1369, 4, 27, 0, 0),
        timezone.datetime(2512, 12, 8, 0, 0),
        timezone.datetime(2170, 1, 18, 0, 0),
        timezone.datetime(1821, 5, 28, 0, 0),
        timezone.datetime(2519, 9, 15, 0, 0),
        timezone.datetime(1721, 7, 19, 0, 0),
        timezone.datetime(2328, 6, 18, 0, 0),
        timezone.datetime(2937, 12, 7, 0, 0),
        timezone.datetime(2555, 11, 10, 0, 0),
        timezone.datetime(2967, 8, 15, 0, 0),
        timezone.datetime(2278, 10, 20, 0, 0),
        timezone.datetime(1158, 5, 23, 0, 0),
        timezone.datetime(2286, 2, 25, 0, 0),
        timezone.datetime(2529, 5, 5, 0, 0),
        timezone.datetime(2307, 2, 3, 0, 0),
        timezone.datetime(1118, 5, 5, 0, 0),
        timezone.datetime(2891, 7, 9, 0, 0),
        timezone.datetime(2579, 6, 8, 0, 0),
        timezone.datetime(2060, 10, 9, 0, 0),
        timezone.datetime(2665, 1, 24, 0, 0),
        timezone.datetime(2096, 8, 15, 0, 0),
        timezone.datetime(2846, 4, 12, 0, 0),
        timezone.datetime(2841, 6, 11, 0, 0),
        timezone.datetime(1429, 5, 27, 0, 0),
        timezone.datetime(1873, 12, 21, 0, 0),
        timezone.datetime(1476, 2, 12, 0, 0),
        timezone.datetime(2061, 1, 1, 0, 0),
        timezone.datetime(2698, 8, 15, 0, 0),
        timezone.datetime(1382, 9, 26, 0, 0)
    ])

    def setUp(self):
        """Add a device with some data points to test."""
        self.user = User(username='test user')
        self.user.save()
        self.device = TrackerDevice(user=self.user, title='test device')
        self.device.save()
        self.client.force_login(self.user)
        for i, date in enumerate(self.TEST_DATA):
            DataPoint(
                time=date,
                lat=i,
                lng=i+30,
                elevation=i+60,
                device=self.device
            ).save()
        url = reverse('detail_device', args=[self.device.pk])
        self.response = self.client.get(url)
        # data should be listed on page by most recent to least
        self.data = self.device.data.order_by('-time')

    def test_title_on_page(self):
        """Test title of device on page."""
        self.assertContains(self.response, self.device.title)

    def test_page_has_data_point_lats(self):
        """Test response has latitudes."""
        for i, datum in enumerate(self.data):
            if i < 10:
                self.assertContains(self.response, datum.lat)
            else:
                self.assertNotContains(self.response, datum.lat)

    def test_page_has_data_point_lngs(self):
        """Test response has longitudes."""
        for i, datum in enumerate(self.data):
            if i < 10:
                self.assertContains(self.response, datum.lng)
            else:
                self.assertNotContains(self.response, datum.lng)

    def test_page_has_data_point_elevation(self):
        """Test response has elevations."""
        for i, datum in enumerate(self.data):
            if i < 10:
                self.assertContains(self.response, datum.elevation)
            else:
                self.assertNotContains(self.response, datum.lng)

    def test_get_page_unauthenticated(self):
        """Test redirects when unauthenticated"""
        self.client.logout()
        url = reverse('detail_device', args=[self.device.pk])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('auth_login'))

    def test_get_page_wrong_user(self):
        """Test redirects when unauthenticated"""
        other_user = User(username='wrong')
        other_user.save()
        self.client.force_login(other_user)
        url = reverse('detail_device', args=[self.device.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class TestDetailRouteView(TestCase):
    """Tests for detail route view."""

    TEST_DATA = map(timezone.make_aware, [
        timezone.datetime(1974, 5, 17, 0, 0),
        timezone.datetime(1369, 4, 27, 0, 0),
        timezone.datetime(2512, 12, 8, 0, 0),
        timezone.datetime(2170, 1, 18, 0, 0),
        timezone.datetime(1821, 5, 28, 0, 0),
        timezone.datetime(2519, 9, 15, 0, 0),
        timezone.datetime(1721, 7, 19, 0, 0),
        timezone.datetime(2328, 6, 18, 0, 0),
        timezone.datetime(2937, 12, 7, 0, 0),
        timezone.datetime(2555, 11, 10, 0, 0),
        timezone.datetime(2967, 8, 15, 0, 0),
        timezone.datetime(2278, 10, 20, 0, 0),
        timezone.datetime(1158, 5, 23, 0, 0),
        timezone.datetime(2286, 2, 25, 0, 0),
        timezone.datetime(2529, 5, 5, 0, 0),
        timezone.datetime(2307, 2, 3, 0, 0),
        timezone.datetime(1118, 5, 5, 0, 0),
        timezone.datetime(2891, 7, 9, 0, 0),
        timezone.datetime(2579, 6, 8, 0, 0),
        timezone.datetime(2060, 10, 9, 0, 0),
        timezone.datetime(2665, 1, 24, 0, 0),
        timezone.datetime(2096, 8, 15, 0, 0),
        timezone.datetime(2846, 4, 12, 0, 0),
        timezone.datetime(2841, 6, 11, 0, 0),
        timezone.datetime(1429, 5, 27, 0, 0),
        timezone.datetime(1873, 12, 21, 0, 0),
        timezone.datetime(1476, 2, 12, 0, 0),
        timezone.datetime(2061, 1, 1, 0, 0),
        timezone.datetime(2698, 8, 15, 0, 0),
        timezone.datetime(1382, 9, 26, 0, 0)
    ])

    def setUp(self):
        """Add a route with some data points to test."""
        self.user = User(username='test user')
        self.user.save()
        self.device = TrackerDevice(user=self.user, title='test device')
        self.device.save()
        for i, date in enumerate(self.TEST_DATA):
            DataPoint(
                time=date,
                lat=i,
                lng=i+30,
                elevation=i+60,
                device=self.device
            ).save()
        start = timezone.make_aware(timezone.datetime(1001, 1, 1))
        end = timezone.make_aware(timezone.datetime(2200, 1, 1))
        self.route = Route(device=self.device, start=start, end=end)
        self.route.save()
        url = reverse('detail_route', args=[self.route.pk])
        self.response = self.client.get(url)

    def test_route_name_on_route_page(self):
        """Test name of route on route page."""
        self.assertContains(self.response, self.route.name)

    def test_route_data_ten_has_ten(self):
        """Test that context['data_ten'] has only 10 things in it."""
        self.assertEqual(len(self.response.context['data_ten']), 10)

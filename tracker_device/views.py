from django import forms
from django.urls import reverse, reverse_lazy
from tracker_device.models import TrackerDevice, Route, DataPoint
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,)


class CreateDeviceView(CreateView):
    """View for creating a new device."""
    model = TrackerDevice
    fields = [
        'device_type',
        'title',
        'description',
        'mode'
    ]
    template_name = 'tracker_device/create_device.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        """Attach user to form."""
        form.instance.user = self.request.user
        return super(CreateDeviceView, self).form_valid(form)


class EditDeviceView(UpdateView):
    """View for editing a device."""
    model = TrackerDevice
    fields = [
        'device_type',
        'title',
        'description',
        'mode'
    ]
    template_name = 'tracker_device/edit_device.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        """Check if the device to edit is owned by user."""
        pk = kwargs.get('pk')
        device = request.user.devices.filter(pk=pk).first()
        if device:
            return super(
                EditDeviceView, self).dispatch(
                    request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class DeleteDeviceView(DeleteView):
    """Delete view for devices."""
    model = TrackerDevice
    template_name = 'tracker_device/delete_device.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        """Check if the device to delete is owned by user."""
        pk = kwargs.get('pk')
        try:
            device = request.user.devices.filter(pk=pk).first()
        except:
            return HttpResponseRedirect(reverse('auth_login'))
        if device:
            return super(
                DeleteDeviceView, self).dispatch(
                    request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class DetailDeviceView(DetailView):
    """Show device details- routes and data points that belong to that
    device and display map"""
    model = TrackerDevice
    template_name = 'tracker_device/detail_device.html'


def verify_route_ownership(user, pk):
    """Verify that the pk matches a route owned by the user.

    Returns HTTPResponseForbidden if the user has routes, otherwise
    redirects to login. If there are no issues, returns None."""
    try:
        route_device = user.devices.filter(routes__pk=pk).first()
        if not route_device:
            return HttpResponseForbidden()
    except AttributeError:
        return HttpResponseRedirect(reverse('auth_login'))


class CreateRouteView(CreateView):
    """Create view for routes."""
    model = Route
    template_name = 'tracker_device/create_route.html'
    success_url = reverse_lazy('profile')
    fields = [
        "name",
        "description",
        "start",
        "end",
        "device",
    ]

    def dispatch(self, request, *args, **kwargs):
        """Check if the route to create is owned by user."""
        auth_errors = verify_route_ownership(request.user, kwargs.get('pk'))
        super_dispatch = super(CreateRouteView, self).dispatch
        return auth_errors or super_dispatch(request, *args, **kwargs)


class EditRouteView(UpdateView):
    """View for editing a route."""
    model = Route
    fields = [
        'name',
        'description',
    ]
    template_name = 'tracker_device/edit_route.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        """Check if the route to edit is owned by user."""
        auth_errors = verify_route_ownership(request.user, kwargs.get('pk'))
        super_dispatch = super(EditRouteView, self).dispatch
        return auth_errors or super_dispatch(request, *args, **kwargs)


class DeleteRouteView(DeleteView):
    """View for deleting a route."""
    model = Route
    template_name = 'tracker_device/delete_route.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        """Check if the route to delete is owned by user."""
        auth_errors = verify_route_ownership(request.user, kwargs.get('pk'))
        super_dispatch = super(DeleteRouteView, self).dispatch
        return auth_errors or super_dispatch(request, *args, **kwargs)


class CreateDataPointForm(forms.ModelForm):
    """Form for adding a data point.

    Has a UUID field on it."""

    class Meta(object):
        model = DataPoint
        exclude = ('device',)
    uuid = forms.UUIDField()

    def clean(self):
        """Ensure UUID being submitted is attached to a device."""
        cleaned_data = super(CreateDataPointForm, self).clean()
        uuid = cleaned_data.get('uuid')
        if TrackerDevice.objects.filter(id_uuid=uuid).count() == 0:
            error = forms.ValidationError('Bad UUID')
            self.add_error('uuid', error)


class CreateDataPointView(CreateView):
    """View for deleting a route."""
    model = Route
    form_class = CreateDataPointForm
    template_name = 'tracker_device/create_data_point.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        """Attach the right device to the form.

        `device` will never be None because this view's form verifies
        that the UUID exists."""
        uuid = form.data['uuid']
        device = TrackerDevice.objects.filter(id_uuid=uuid).first()
        form.instance.device = device
        return super(CreateDataPointView, self).form_valid(form)

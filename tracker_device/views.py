from django.urls import reverse, reverse_lazy
from tracker_device.models import TrackerDevice, Route
from django.http import HttpResponseForbidden, HttpResponseRedirect
from uuid import uuid4
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView)


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
        """Attach user and new uuid to user."""
        form.instance.user = self.request.user
        form.instance.uuid = uuid4()
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
        """Check if the route to delete is owned by user."""
        pk = kwargs.get('pk')
        try:
            route_device = request.user.devices.filter(routes__pk=pk).first()
            if not route_device:
                return HttpResponseForbidden()
        except AttributeError:
            return HttpResponseRedirect(reverse('auth_login'))
        return super(
                CreateRouteView, self).dispatch(
                    request, *args, **kwargs)


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
        """Check if the route to delete is owned by user."""
        pk = kwargs.get('pk')
        try:
            route_device = request.user.devices.filter(routes__pk=pk).first()
            if not route_device:
                return HttpResponseForbidden()
        except AttributeError:
            return HttpResponseRedirect(reverse('auth_login'))
        return super(
                EditRouteView, self).dispatch(
                    request, *args, **kwargs)


class DeleteRouteView(DeleteView):
    """View for deleting a route."""
    model = Route
    template_name = 'tracker_device/delete_route.html'
    success_url = reverse_lazy('profile')

from django.urls import reverse_lazy
from tracker_device.models import TrackerDevice
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
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


class DeleteDeviceView(LoginRequiredMixin, DeleteView):
    """Delete view for devices."""
    model = TrackerDevice
    template_name = 'tracker_device/delete_device.html'
    success_url = reverse_lazy('profile')

    # def dispatch(self, request, *args, **kwargs):
    #     """Check if the device to delete is owned by user."""
    #     pk = kwargs.get('pk')
    #     device = request.user.devices.filter(pk=pk).first()
    #     if device:
    #         return super(
    #             DeleteDeviceView, self).dispatch(
    #                 request, *args, **kwargs)
    #     else:
    #         return HttpResponseForbidden()

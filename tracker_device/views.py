from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from tracker_device.models import TrackerDevice
from uuid import uuid4


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

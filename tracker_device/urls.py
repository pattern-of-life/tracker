from django.conf.urls import url
from tracker_device.views import CreateDeviceView

urlpatterns = [
    url(r'^create$', CreateDeviceView.as_view(), name='create_device'),
]

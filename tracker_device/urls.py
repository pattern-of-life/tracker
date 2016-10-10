from django.conf.urls import url
from tracker_device.views import CreateDeviceView, EditDeviceView

urlpatterns = [
    url(r'create/$', CreateDeviceView.as_view(), name='create_device'),
    url(r'(?P<pk>[0-9]+)/edit/$', EditDeviceView.as_view(), name='edit_device'),
]

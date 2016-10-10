from django.conf.urls import url
from tracker_device.views import (
    CreateDeviceView,
    EditDeviceView,
    DeleteDeviceView,
    CreateRouteView,
)

urlpatterns = [
    url(
        r'create/$',
        CreateDeviceView.as_view(),
        name='create_device'
        ),
    url(
        r'(?P<pk>[0-9]+)/edit/$',
        EditDeviceView.as_view(),
        name='edit_device'
        ),
    url(
        r'(?P<pk>[0-9]+)/delete/$',
        DeleteDeviceView.as_view(),
        name='delete_device'
        ),
    url(
        r'create/route/$',
        CreateRouteView.as_view(),
        name='create_route'
        ),
]

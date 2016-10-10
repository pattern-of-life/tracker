from django.conf.urls import url
from tracker_device.views import (
    CreateDeviceView,
    EditDeviceView,
    DeleteDeviceView,
    CreateRouteView,
    EditRouteView,
    DeleteRouteView,
)

urlpatterns = [
    url(
        r'^create/$',
        CreateDeviceView.as_view(),
        name='create_device'
        ),
    url(
        r'^(?P<pk>[0-9]+)/edit/$',
        EditDeviceView.as_view(),
        name='edit_device'
        ),
    url(
        r'^(?P<pk>[0-9]+)/delete/$',
        DeleteDeviceView.as_view(),
        name='delete_device'
        ),
    url(
        r'^route/create/$',
        CreateRouteView.as_view(),
        name='create_route'
        ),
    url(
        r'^route/(?P<pk>[0-9]+)/edit/$',
        EditRouteView.as_view(),
        name='edit_route'
        ),
    url(
        r'^route/(?P<pk>[0-9]+)/delete/$',
        DeleteRouteView.as_view(),
        name='delete_route'
        ),
]

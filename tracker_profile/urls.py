from django.conf.urls import url
from tracker_profile.views import ProfileView

urlpatterns = [
    url(r'^profile$', ProfileView.as_view(), name='profile')
]

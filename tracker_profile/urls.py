from django.conf.urls import url
from tracker_profile.views import ProfileView, EditProfileView

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='profile'),
    url(r'edit$', EditProfileView.as_view(), name='edit_profile'),
]

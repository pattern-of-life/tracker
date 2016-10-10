from django.views.generic import DetailView, UpdateView
from tracker_profile.models import TrackerProfile
from django.urls import reverse_lazy


class ProfileView(DetailView):
    """View for profile."""
    model = TrackerProfile
    template_name = "tracker_profile/profile.html"

    def get_object(self):
        return self.request.user.profile


class EditProfileView(UpdateView):
    """View for profile."""
    model = TrackerProfile
    fields = [
        'bio',
        'access_level',
        'lat',
        'lng',
        'street_address',
        'website',
        'social_media',
    ]
    template_name = "tracker_profile/edit_profile.html"

    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

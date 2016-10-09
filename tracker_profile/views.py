from django.views.generic.detail import DetailView
from tracker_profile.models import TrackerProfile


class ProfileView(DetailView):
    """View for profile."""
    model = TrackerProfile
    template_name = "tracker_profile/profile.html"

    def get_object(self):
        return self.request.user.profile

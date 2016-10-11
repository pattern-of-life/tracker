from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    """Create HomeView class."""
    template_name = 'tracker/home.html'


class AboutView(TemplateView):
    """Create AboutView class."""
    template_name = 'tracker/about.html'

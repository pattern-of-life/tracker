from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    """Create HomeView class."""
    template_name = 'tracker/home.html'

    def get_context_data(self, **kwargs):
        """Modify context returned to this view."""
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

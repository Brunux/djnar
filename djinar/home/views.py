from django.views.generic import TemplateView

# Create your views here.


class HomeView(TemplateView):
    """[summary]

    [description]

    Extends:
        TemplateView
    """
    template_name = 'home.html'

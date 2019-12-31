from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView

from .models import Contact
from .serializers import ContactSerializer


class ContactsView(TemplateView):
    """[summary]
    Servers the base web page for contacts.

    [description]
    """
    template_name = 'contacts.html'


class ContactItemsView(ListAPIView):
    """[summary]
    Gets contacts items paginated
    [description]
    """
    serializer_class = ContactSerializer

    def get_queryset(self):
        """
        This view should return a list of all the contacts
        for the currently authenticated user.
        """
        user = self.request.user
        return Contact.objects.filter(owner=user).order_by('-modified')

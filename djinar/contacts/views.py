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
    Gets contacts items paginated in descending order last
    modified.

    [description]
    This view should return a list of all the contacts for the currently
    authenticated user.
    """
    serializer_class = ContactSerializer

    def get_queryset(self):
        """
        Return `user` contacts only.
        """
        return Contact.objects.filter(
            owner=self.request.user
        ).order_by('-modified')

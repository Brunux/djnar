from django.views.generic import TemplateView
from rest_framework import filters
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from .models import Contact
from .serializers import ContactSerializer, ContactCreateSerializer


class ContactsView(TemplateView):
    """[summary]
    Servers the base web page for contacts.

    [description]
    """
    template_name = 'contacts.html'


class ContactItemsView(ListAPIView):
    """[summary]
    Gets contacts items paginated in descending order and may be
    filtered.

    [description]
    This view should return a list of contacts for the currently
    authenticated user.

    Extends:
        ListAPIView
    """
    serializer_class = ContactSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = (
        'name',
        'email',
        'company',
        'job_title',
    )

    def get_queryset(self):
        """
        Return `user` contacts only.
        """
        return Contact.objects.filter(
            owner=self.request.user
        ).order_by('-modified')


class ContactItemCreateView(CreateAPIView):
    """[summary]
    Creates a new contact item.

    [description]
    This view should validate and create a new contact item linking
    the item to the current authenticate user.

    Extends:
        CreateAPIView
    """
    serializer_class = ContactCreateSerializer

    def create(self, request, *args, **kwargs):
        request.data.update({"owner": self.request.user.pk})
        return super().create(request, *args, **kwargs)


class EditContactItemView(RetrieveUpdateDestroyAPIView):
    """[summary]
    Edits or Deletes a contact item.

    [description]
    This View updates fields for a contact item it can also delete a
    contact item.

    Extends:
        RetrieveUpdateDestroyAPIView
    """
    serializer_class = ContactSerializer
    lookup_field = "pid"

    def get_queryset(self):
        """
        Return `user` contacts only.
        """
        return Contact.objects.filter(
            owner=self.request.user
        )

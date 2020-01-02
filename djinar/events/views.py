from datetime import datetime

from django.views.generic import TemplateView
from rest_framework import filters
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from .models import Event
from .serializers import EventSerializer, EventCreateSerializer


class EventsView(TemplateView):
    """[summary]
    Servers main events FE app.

    [description]
    """
    template_name = 'events.html'


class EventItemsView(ListAPIView):
    """[summary]
    Gets Events items paginated in descending order and may be
    filtered.

    [description]
    This view should return a list of Events for the currently
    authenticated user.

    Extends:
        ListAPIView
    """
    serializer_class = EventSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = (
        'title',
        'attendants__name',
        'attendants__email',
        'notes',
    )

    def get_queryset(self):
        """
        Return `user` Events only.

        Filtering is possible by init and end dates e.g.
        ?init=2019-12-31&end=2020-01-01 those dates should be in UTC.
        """
        return Event.objects.filter(
            owner=self.request.user
        ).order_by('-modified').prefetch_related('attendants')


class EventItemsDateView(ListAPIView):
    """[summary]
    Gets Events items paginated in descending order and may be
    filtered.

    [description]
    This view should return a list of Events for the currently
    authenticated user.

    Extends:
        ListAPIView
    """
    serializer_class = EventSerializer
    pagination_class = None

    def get_queryset(self):
        """
        Return `user` Events only.

        Filtering is possible by init and end dates e.g.
        ?init=2019-12-31&end=2020-01-01 those dates should be in UTC.
        """
        query_set = Event.objects.filter(
            owner=self.request.user
        ).order_by('-modified')

        # Dates should be in YYYY-MM-DD and UTC.
        initial_date = self.request.query_params.get('init', None)
        end_date = self.request.query_params.get('end', None)

        if not initial_date or not end_date:
            return Event.objects.none()

        try:
            initial_date = datetime.strptime(
                f"{initial_date} 0:0:0", "%Y-%m-%d %H:%M:%S",
            )
            end_date = datetime.strptime(
                f"{end_date} 23:59:59", "%Y-%m-%d %H:%M:%S",
            )
        except Exception:
            return Event.objects.none()

        return query_set.filter(
            date__gte=initial_date,
            date__lte=end_date
        ).prefetch_related('attendants')


class EventItemCreateView(CreateAPIView):
    """[summary]
    Creates a new Event item.

    [description]
    This view should validate and create a new Event item linking
    the item to the current authenticate user.

    Extends:
        CreateAPIView
    """
    serializer_class = EventCreateSerializer

    def create(self, request, *args, **kwargs):
        request.data.update({"owner": self.request.user.pk})
        return super().create(request, *args, **kwargs)


class EventItemEditView(RetrieveUpdateDestroyAPIView):
    """[summary]
    Edits or Deletes a Event item.

    [description]
    This View updates fields for a Event item it can also delete a
    Event item.

    Extends:
        RetrieveUpdateDestroyAPIView
    """
    serializer_class = EventCreateSerializer
    lookup_field = "pid"

    def get_queryset(self):
        """
        Return `user` Events only.
        """
        return Event.objects.filter(
            owner=self.request.user
        )

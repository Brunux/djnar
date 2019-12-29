from django.views.generic import TemplateView


class EventsView(TemplateView):
    """[summary]

    [description]
    """
    template_name = 'events.html'
    extra_context = {
        'events': [
            {
                'title': "Event #1",
                "date": "19-04-21",
            },
            {
                'title': "Event #2",
                "date": "19-04-22",
            },
            {
                'title': "Event #3",
                "date": "19-04-23",
            }
        ]
    }


class EventView(TemplateView):
    """[summary]

    [description]
    """
    template_name = 'event.html'
    extra_context = {
        'event': [
            {
                'title': "Event #1",
                "date": "19-04-21",
            }
        ]
    }

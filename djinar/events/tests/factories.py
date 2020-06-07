"""Events factories that you love."""
import factory
import factory.fuzzy

from django.contrib.auth import get_user_model

from ..models import Event


class EventFactory(factory.django.DjangoModelFactory):
    """Factory for your `Events` tests.
    Pass any of the attributes on instantiation to overwrite defaults e.g.

    ```
    test_event = EventFactory(title="Test Event Title")
    ```

    If passing `attendants` make sure to pass a QuerySet.
    """
    title = factory.LazyAttribute(lambda event: f"{event.owner.name} Meeting")
    date = factory.Faker('date')
    duration = factory.fuzzy.FuzzyInteger(30)
    notes = factory.Faker(
        'paragraph',
        nb_sentences=3,
        variable_nb_sentences=True,
    )
    owner = factory.Iterator(
        get_user_model().objects.all()
    )

    @factory.post_generation
    def attendants(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            # A list of attendants were passed in, use them
            for attendant in extracted:
                self.attendants.add(attendant)

    class Meta:
        model = Event

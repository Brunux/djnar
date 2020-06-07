"""Events model method tests."""
from django.test import TestCase

from djinar.users.tests.factories import UserFactory
from djinar.contacts.tests.factories import ContactFactory

from .factories import EventFactory


class EventModelTestCases(TestCase):
    """Main test cases for `Event` model."""

    def setUp(self, *args, **kwargs):
        """Adds owner from `UserFactory` and attendants from `ContactFactory`."""

        self.owner = UserFactory()
        self.attendants = [ContactFactory(owner=self.owner) for _ in range(6)]
        return super().setUp(*args, **kwargs)

    def test__str__(self):
        """Should validate correct value for `__str__()`"""

        event_title = "Test Event"
        event = EventFactory(
            title=event_title,
            attendants=self.attendants,
            owner=self.owner,
        )
        self.assertEqual(event_title, str(event))

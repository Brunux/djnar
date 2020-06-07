"""Contacts model method tests."""
from django.test import TestCase
from .factories import ContactFactory
from djinar.users.tests.factories import UserFactory


class ContactModelTestCases(TestCase):
    """Main test cases for `Contact` model."""

    def setUp(self, *args, **kwargs):
        """Adds owner from `UserFactory`."""

        self.owner = UserFactory()
        return super().setUp(*args, **kwargs)

    def test__str__(self):
        """Should validate correct value for `__str__()`"""

        contact_email = "test@example.com"
        contact = ContactFactory(email=contact_email, owner=self.owner)
        self.assertEqual(contact_email, str(contact))

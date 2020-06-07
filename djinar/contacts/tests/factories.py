"""Factories that you love."""
import factory
import factory.fuzzy
from django.contrib.auth import get_user_model

from ..models import Contact


class ContactFactory(factory.django.DjangoModelFactory):
    """Factory for your `Contacts` tests.
    Pass any of the attributes on instantiation to overwrite defaults e.g.

    test_contact = ContactFactory(owner=user_instance)
    """
    name = factory.Faker('name')
    job_title = factory.fuzzy.FuzzyText()
    company = factory.Faker('company')
    email = factory.Faker('email')
    contact_number = factory.Faker('phone_number')
    notes = factory.Faker(
        'paragraph',
        nb_sentences=3,
        variable_nb_sentences=True,
    )
    owner = factory.Iterator(
        get_user_model().objects.all()
    )

    class Meta:
        model = Contact

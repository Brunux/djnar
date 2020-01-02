from django.contrib.auth import get_user_model
from django.test import TestCase

from djinar.core.utils import create_user_util
from djinar.contacts.models import Contact


def create_test_contact():
    """[summary]
    Creates a dummy contact and returns it.
    [description]
    """
    User = get_user_model()
    user = User.objects.last()
    if not user:
        user = create_user_util()

    contact_data = {
        "name": "TestCase",
        "job_title": "Sr. Python Developer",
        "company": "Django",
        "email": "test@case.dj",
        "contact_number": "+523319442828",
        "notes": "This is a test",
        "owner": user,
    }
    contact = Contact.objects.create(**contact_data)
    return contact

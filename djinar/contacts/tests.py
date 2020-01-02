from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from djinar.core.utils import create_user_util, TEST_USERNAME, TEST_PASSWORD
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


class ContactTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.last()
        if not user:
            user = create_user_util()
        self.user = user
        is_logedin = self.client.login(
            username=TEST_USERNAME, password=TEST_PASSWORD
        )
        if not is_logedin:
            raise Exception("Unable to login test client")
        self.contact_data = contact_data = {
            "job_title": "Sr. Python Developer",
            "company": "Django",
            "email": "test@case.dj",
            "contact_number": "+523319442828",
            "notes": "This is a test",
            "owner": user.pk,
        }

    def test_contact_creation(self):
        """[summary]
        Test contact creation endpoint.
        [description]
        """
        contact_name = "Test Contact Creation"
        contact_data = self.contact_data
        contact_data.update({
            "name": contact_name,
        })
        endpoint = reverse("contacts:create")
        resp = self.client.post(endpoint, contact_data, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            msg=f"Contact not created, status_code: {resp.status_code}",
        )
        contact = Contact.objects.get(name=contact_name)
        contact.delete()

    def test_contact_retrieve(self):
        """[summary]
        Test contact retrieve endpoint.
        [description]
        """
        contact_name = "Test Contact for Retrieve"
        contact_data = self.contact_data
        contact_data.update({
            "name": contact_name,
        })
        endpoint = reverse("contacts:create")
        resp = self.client.post(endpoint, contact_data, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            msg=f"Contact not created, status_code: {resp.status_code}",
        )
        contact = Contact.objects.get(name=contact_name)

        endpoint = reverse("contacts:items")
        contact_search_name = {
            "search": contact.name
        }
        resp = self.client.get(endpoint, contact_search_name, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Contact not retrieve by name, status_code {resp.status_code}",
        )
        contact_search_email = {
            "search": contact.email
        }
        resp = self.client.get(endpoint, contact_search_email, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Contact not retrieve by email, status_code {resp.status_code}",
        )
        contact_search_company = {
            "search": contact.company
        }
        resp = self.client.get(endpoint, contact_search_company, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Contact not retrieve by company, status_code {resp.status_code}",
        )
        contact_search_job_title = {
            "search": contact.job_title
        }
        resp = self.client.get(endpoint, contact_search_job_title, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Contact not retrieve by job_title, status_code {resp.status_code}",
        )
        contact.delete()

    def test_contact_update(self):
        """[summary]
        Test contact creation endpoint.
        [description]
        """
        contact_name = "Test Contact Creation for Update"
        contact_data = self.contact_data
        contact_data.update({
            "name": contact_name,
        })
        endpoint = reverse("contacts:create")
        resp = self.client.post(endpoint, contact_data, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            msg=f"Contact not created, status_code: {resp.status_code}",
        )
        contact = Contact.objects.get(name=contact_name)

        endpoint = reverse("contacts:edit", args=[contact.pid])
        contact_name = "Test Contact Updated"
        contact_data = {
            "name": contact_name,
        }
        resp = self.client.patch(endpoint, contact_data, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Contact not updated, status_code {resp.status_code}",
        )
        contact = Contact.objects.get(name=contact_name)
        contact.delete()

    def test_contact_deletion(self):
        """[summary]
        Test contact deletion endpoint.
        [description]
        """
        contact_name = "Test Contact for Deletion"
        contact_data = self.contact_data
        contact_data.update({
            "name": contact_name,
        })
        endpoint = reverse("contacts:create")
        resp = self.client.post(endpoint, contact_data, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            msg=f"Contact not created, status_code: {resp.status_code}",
        )
        contact = Contact.objects.get(name=contact_name)

        endpoint = reverse("contacts:edit", args=[contact.pid])
        resp = self.client.delete(endpoint, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_204_NO_CONTENT,
            msg=f"Contact not delete, status_code {resp.status_code}",
        )
        event_qs = Contact.objects.filter(name=contact_name)
        self.assertFalse(event_qs.exists())

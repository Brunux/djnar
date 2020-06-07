from djinar.contacts.models import Contact
from django.urls import reverse
from djinar.users.tests.factories import UserFactory
from rest_framework import status
from rest_framework.test import APITestCase


class ContactTestCase(APITestCase):
    def setUp(self):
        user_password = "abc123"
        self.user = UserFactory(password=user_password)
        is_logedin = self.client.login(
            username=self.user.username, password=user_password
        )
        if not is_logedin:
            raise Exception("Unable to login test client")

        self.contact_data = {
            "job_title": "Sr. Python Developer",
            "company": "Django",
            "email": "test@case.dj",
            "contact_number": "+523319442828",
            "notes": "This is a test",
            "owner": self.user.pk,
        }

    def test_contact_creation(self):
        """Test contact creation endpoint."""

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
        """Test contact retrieve endpoint."""

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
            msg=f"Contact not retrieved by name, status_code {resp.status_code}",
        )
        self.assertTrue(
            resp.json()["results"][0],
            msg="Contact not retrieved by name",
        )
        contact_search_email = {
            "search": contact.email
        }
        resp = self.client.get(endpoint, contact_search_email, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Contact not retrieved by email, status_code {resp.status_code}",
        )
        self.assertTrue(
            resp.json()["results"][0],
            msg="Contact not retrieved by email",
        )
        contact_search_company = {
            "search": contact.company
        }
        resp = self.client.get(endpoint, contact_search_company, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Contact not retrieved by company, status_code {resp.status_code}",
        )
        self.assertTrue(
            resp.json()["results"][0],
            msg="Contact not retrieved by company",
        )
        contact_search_job_title = {
            "search": contact.job_title
        }
        resp = self.client.get(endpoint, contact_search_job_title, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Contact not retrieved by job_title, status_code {resp.status_code}",
        )
        self.assertTrue(
            resp.json()["results"][0],
            msg="Contact not retrieved by job_title",
        )
        contact.delete()

    def test_contact_update(self):
        """Test contact creation endpoint."""
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
        """Test contact deletion endpoint."""
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

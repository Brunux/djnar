import uuid

from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from djinar.core.utils import TEST_USERNAME, TEST_PASSWORD
from djinar.contacts.tests import create_test_contact

from .models import Event


class EventTestCase(APITestCase):
    def setUp(self):
        self.contact = create_test_contact()
        is_logedin = self.client.login(
            username=TEST_USERNAME, password=TEST_PASSWORD
        )
        if not is_logedin:
            raise Exception("Unable to login test client")
        self.event_data = {
            "date": timezone.now(),
            "duration": "30",
            "notes": "This is test event",
        }

    def test_event_creation(self):
        """[summary]
        Test event creation endpoint.
        [description]
        """
        event_title = "Test Event Creation"
        event_data = self.event_data
        event_data.update({
            "title": event_title,
            "attendants": [{"pid": str(self.contact.pid)}],
        })
        endpoint = reverse("events:create")
        resp = self.client.post(endpoint, event_data, format='json')
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            msg=f"Event not created status code: {resp.status_code}",
        )
        event = Event.objects.get(title=event_title)
        attendants_count = event.attendants.count()
        self.assertEqual(
            attendants_count,
            1,
            msg=f"Invalid attendants {attendants_count}"
        )
        event.delete()

    def test_event_creation_invalid_attendants(self):
        """[summary]
        Test event creation endpoint with invalid attendants.
        [description]
        """
        event_title = "Test Event Invalid Attendants"
        event_data = self.event_data
        event_data.update({
            "title": event_title,
            "attendants": [
                {"pid": str(uuid.uuid4())},
            ],
        })
        endpoint = reverse("events:create")
        resp = self.client.post(endpoint, event_data, format='json')
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            msg=f"Event not created status code: {resp.status_code}",
        )
        event = Event.objects.get(title=event_title)
        attendants_count = event.attendants.count()
        self.assertEqual(
            attendants_count,
            0,
            msg=f"Invalid attendants {attendants_count}"
        )
        event.delete()

    def test_event_retrieve(self):
        """[summary]
        Test event retrieve endpoint.
        [description]
        """
        event_title = "Test Event for Retrieve"
        event_data = self.event_data
        event_data.update({
            "title": event_title,
            "attendants": [{"pid": str(self.contact.pid)}],
        })
        endpoint = reverse("events:create")
        resp = self.client.post(endpoint, event_data, format='json')
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            msg=f"Event not created status code: {resp.status_code}",
        )
        event = Event.objects.get(title=event_title)
        endpoint = reverse("events:items")

        event_search_title = {
            "search": event.title
        }
        resp = self.client.get(endpoint, event_search_title, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Event not retrieved by title, status_code {resp.status_code}",
        )
        self.assertTrue(
            resp.json()["results"][0],
            msg="Event not retrieved by title",
        )

        event_search_attendants_name = {
            "search": event.attendants.first().name
        }
        resp = self.client.get(endpoint, event_search_attendants_name, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Event not retrieved by attendants_name, status_code {resp.status_code}",
        )
        self.assertTrue(
            resp.json()["results"][0],
            msg="Event not retrieved by attendants_name",
        )

        event_search_attendants_email = {
            "search": event.attendants.first().email
        }
        resp = self.client.get(endpoint, event_search_attendants_email, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Event not retrieved by attendants_email, status_code {resp.status_code}",
        )
        self.assertTrue(
            resp.json()["results"][0],
            msg="Event not retrieved by attendants_email",
        )

        event_search_notes = {
            "search": event.notes
        }
        resp = self.client.get(endpoint, event_search_notes, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Event not retrieved by notes, status_code {resp.status_code}",
        )
        self.assertTrue(
            resp.json()["results"][0],
            msg="Event not retrieved by notes",
        )
        event.delete()

    def test_event_retrieve_by_date(self):
        """[summary]
        Test event retrieve by date endpoint.
        [description]
        Dates should be in YYYY-MM-DD and UTC.
        """
        event_title = "Test Event Creation"
        event_data = self.event_data
        event_data.update({
            "title": event_title,
            "attendants": [{"pid": str(self.contact.pid)}],
        })
        endpoint = reverse("events:create")
        init_date = timezone.now()
        resp = self.client.post(endpoint, event_data, format='json')
        end_date = timezone.now()
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            msg=f"Event not created status code: {resp.status_code}",
        )
        event = Event.objects.get(title=event_title)
        endpoint = reverse("events:items_date")

        event_search_date = {
            # Dates should be in YYYY-MM-DD and UTC.
            "init": str(init_date).split()[0],
            "end": str(end_date).split()[0],
        }
        resp = self.client.get(endpoint, event_search_date, format="json")
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Event not retrieved by date, status_code {resp.status_code}",
        )
        self.assertTrue(
            resp.json()[0],
            msg="Event not retrieved by date",
        )
        event.delete()

    def test_event_update(self):
        """[summary]
        Test event update endpoint with `patch`.
        [description]
        """
        event_title = "Test Event Creation for Update"
        event_data = self.event_data
        event_data.update({
            "title": event_title,
            "attendants": [{"pid": str(self.contact.pid)}],
        })
        endpoint = reverse("events:create")
        resp = self.client.post(endpoint, event_data, format='json')
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            msg=f"Event not created status code: {resp.status_code}",
        )
        event = Event.objects.get(title=event_title)
        endpoint = reverse("events:edit", args=[event.pid])
        event_title = "Test Event Updated !K"
        event_data = {
            "title": event_title,
            "attendants": [],
        }
        resp = self.client.patch(endpoint, event_data, format='json')
        self.assertEqual(
            resp.status_code,
            status.HTTP_200_OK,
            msg=f"Event not updated status code: {resp.status_code}",
        )
        event = Event.objects.get(title=event_title)
        attendants_count = event.attendants.count()
        self.assertEqual(
            attendants_count,
            0,
            msg=f"Invalid attendants {attendants_count}"
        )
        event.delete()

    def test_event_deletion(self):
        """[summary]
        Test event deletion endpoint.
        [description]
        """
        event_title = "Test Event for Deletion"
        event_data = self.event_data
        event_data.update({
            "title": event_title,
            "attendants": [{"pid": str(self.contact.pid)}],
        })
        endpoint = reverse("events:create")
        resp = self.client.post(endpoint, event_data, format='json')
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            msg=f"Event not created status code: {resp.status_code}",
        )
        event = Event.objects.get(title=event_title)
        endpoint = reverse("events:edit", args=[event.pid])
        resp = self.client.delete(endpoint, format='json')
        self.assertEqual(
            resp.status_code,
            status.HTTP_204_NO_CONTENT,
            msg=f"Event not deleted status code: {resp.status_code}",
        )
        event_qs = Event.objects.filter(title=event_title)
        self.assertFalse(event_qs.exists())

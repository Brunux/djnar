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

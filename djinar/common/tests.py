from rest_framework.test import APITestCase

from djinar.users.tests.factories import UserFactory


class APILoggedInTest(APITestCase):
    """Adds self.user logged in to make test with an authenticated user."""

    def setUp(self, *args, **kwargs):
        user_password = "abc123"
        self.user = UserFactory(password=user_password)
        is_logedin = self.client.login(
            username=self.user.username, password=user_password
        )
        if not is_logedin:
            raise Exception("Unable to login test client")
        return super().setUp(*args, **kwargs)

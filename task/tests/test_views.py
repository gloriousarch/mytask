from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LoginTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="testuser", password="testpass123*")
        User.objects.create_user(username="testuser1", password="testpass123*", is_active=False)

    def test_default_unauthorised(self):
        response = self.client.get(reverse("task:login-test"))
        self.assertEquals(403, response.status_code)

    def test_login_page(self):
        response = self.client.get(reverse("task:login"))
        self.assertEquals(200, response.status_code)

    def test_login_success(self):
        response = self.client.post(reverse("task:login"), dict(username="testuser", password="testpass123*"))
        self.assertEquals(302, response.status_code)

    def test_login_disabled(self):
        response = self.client.post(reverse("task:login"), dict(username="testuser1", password="testpass123*"))
        self.assertIn(b"Invalid", response.content)

    def test_wrong_credentials(self):
        response = self.client.post(reverse("task:login"), dict(username="testuser1", password="test"))
        self.assertIn(b"Invalid", response.content)

    def test_authorised(self):
        self.client.post(reverse("task:login"), dict(username="testuser", password="testpass123*"))
        response = self.client.get(reverse("task:login-test"))
        self.assertEquals(200, response.status_code)

    def test_logout_unauthorised(self):
        self.client.post(reverse("task:login"), dict(username="testuser", password="testpass123*"))
        response = self.client.get(reverse("task:login-test"))
        self.assertEquals(200, response.status_code)

        self.client.get(reverse("task:logout"))
        response = self.client.get(reverse("task:login-test"))
        self.assertEquals(403, response.status_code)

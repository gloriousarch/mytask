from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from task.models import UserProfile


class PageTest(TestCase):
    def test_login_page(self):
        response = self.client.get(reverse("task:login"))
        self.assertEquals(200, response.status_code)

    def test_index_page(self):
        response = self.client.get(reverse("task:index"))
        self.assertEquals(200, response.status_code)

    def test_about_page(self):
        response = self.client.get(reverse("task:about"))
        self.assertEquals(200, response.status_code)

    def test_register_page(self):
        response = self.client.get(reverse("task:register"))
        self.assertEquals(200, response.status_code)


class LoginTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="testuser", password="testpass123*")
        User.objects.create_user(username="testuser1", password="testpass123*", is_active=False)

    def test_default_unauthorised(self):
        response = self.client.get(reverse("task:login-test"))
        self.assertEquals(403, response.status_code)

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


class RegisterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="testuser", password="testpass123*")

    def test_register_empty(self):
        response = self.client.post(reverse("task:register"))
        self.assertEquals(400, response.status_code)

    def test_register_no_pass(self):
        response = self.client.post(reverse("task:register"), dict(username="user1", first_name="Test",
                                                                   last_name="User", email="tester@mytask.co.uk"))
        self.assertEquals(400, response.status_code)

    def test_register_existing_username(self):
        response = self.client.post(reverse("task:register"), dict(username="testuser", password="mypass!"))
        self.assertEquals(400, response.status_code)

    def test_register_success(self):
        response = self.client.post(reverse("task:register"), dict(username="testuser1", password="test"))
        self.assertEquals(302, response.status_code)

    def test_register_login(self):
        self.client.post(reverse("task:register"), dict(username="testuser1", password="test"))
        response = self.client.post(reverse("task:login"), dict(username="testuser1", password="test"))
        self.assertEquals(302, response.status_code)

    def test_register_login_authorisation(self):
        response = self.client.post(reverse("task:register"), dict(username="testuser1", password="test"))
        self.client.post(response.url, dict(username="testuser1", password="test"))
        response = self.client.get(reverse("task:login-test"))
        self.assertEquals(200, response.status_code)

    def test_profile_creation(self):
        self.client.post(reverse("task:register"), dict(username="testuser1", password="test"))
        self.assertRaises(ObjectDoesNotExist, UserProfile.objects.get, user__username="testuser1s")
        try:
            UserProfile.objects.get(user__username="testuser1")
        except ObjectDoesNotExist:
            self.fail("New user profile does not exist.")


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="testuser", password="testpass123*")

    def authenticate(self):
        self.client.post(reverse("task:login"), dict(username="testuser", password="testpass123*"))

    def test_change_password(self):
        self.authenticate()
        # Change password, logout, and login with new credentials
        self.client.post(reverse("task:changepassword"), dict(password="newpass"))
        self.client.get(reverse("task:logout"))
        response = self.client.post(reverse("task:login"), dict(username="testuser", password="newpass"))
        self.assertEquals(302, response.status_code)

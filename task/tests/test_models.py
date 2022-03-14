from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from task.models import UserProfile


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="testuser", password="testpass123*")

    def setUp(self):
        self.user = User.objects.first()

    def test_str(self):
        profile = UserProfile(user=self.user, phone_number="+441234567890", tasks_posted=6, tasks_received=2)
        self.assertEquals(self.user.username, str(profile))

    def test_wrong_number_format(self):
        profile = UserProfile(user=self.user, phone_number="1452")
        self.assertRaises(ValidationError, profile.full_clean)

    def test_number_length_short(self):
        profile = UserProfile(user=self.user, phone_number="+12345678")
        self.assertRaises(ValidationError, profile.full_clean)

    def test_number_length_long(self):
        profile = UserProfile(user=self.user, phone_number="+12345678901234567")
        self.assertRaises(ValidationError, profile.full_clean)

    def test_number_correct(self):
        profile = UserProfile(user=self.user, phone_number="+441234567890")
        try:
            profile.full_clean()
        except ValidationError:
            self.fail("Correct number format validation failed.")

    def test_default_values(self):
        profile = UserProfile(user=self.user)
        self.assertEquals(0, profile.tasks_posted)
        self.assertEquals(0, profile.tasks_received)
        self.assertEquals(0, profile.tasks_completed)
        self.assertEquals('', profile.phone_number)
        self.assertRaises(ValueError, profile.picture._get_file)

    def test_user_relation(self):
        profile = UserProfile(user=self.user)
        self.assertEquals("testuser", profile.user.username)

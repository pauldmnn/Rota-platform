from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import time, date, timedelta

from rota.models import Rota, Request, StaffProfile

User = get_user_model()


class RotaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='john_doe', password='testpassword'
        )

        self.rota = Rota.objects.create(
            user=self.user,
            date=date.today(),
            shift_type='Long Day',
        )

    def test_rota_creation(self):
        """
        Ensure a Rota object is correctly created and has default values.
        """
        self.assertIsNotNone(self.rota.id)
        self.assertEqual(self.rota.user, self.user)
        self.assertEqual(self.rota.shift_type, 'Long Day')
        self.assertIsNone(self.rota.start_time)
        self.assertIsNone(self.rota.end_time)
        self.assertFalse(self.rota.is_updated)

    def test_rota_str_method_default(self):
        """
        Test the default __str__ method for non-Custom shifts.
        """
        expected_str = f"{self.user.get_full_name()} - {self.rota.date} - {self.rota.shift_type}"
        self.assertEqual(str(self.rota), expected_str)

    def test_rota_str_method_custom_shift(self):
        """
        Test the __str__ method when shift_type is "Custom" and has start/end times.
        """
        self.rota.shift_type = "Custom"
        self.rota.start_time = time(9, 0)
        self.rota.end_time = time(17, 30)
        self.rota.save()

        expected_str = (
            f"{self.user.get_full_name()} - {self.rota.date} - Custom "
            f"({self.rota.start_time} to {self.rota.end_time})"
        )
        self.assertEqual(str(self.rota), expected_str)


class RequestModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='jane_doe', password='janepass'
        )
        self.request_obj = Request.objects.create(
            user=self.user,
            date=date.today() + timedelta(days=1),
            comment='Need a day off',
        )

    def test_request_creation(self):
        """
        Ensure a Request object is created with the correct defaults.
        """
        self.assertIsNotNone(self.request_obj.id)
        self.assertEqual(self.request_obj.user, self.user)
        self.assertEqual(self.request_obj.status, 'Pending')  
        self.assertIsNone(self.request_obj.admin_comment)
        self.assertIsNotNone(self.request_obj.created_at)


class StaffProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='profile_user', password='profilepass'
        )

    def test_staff_profile_auto_creation(self):
        """
        Verify a StaffProfile is automatically created via the post_save signal.
        """
        self.assertTrue(StaffProfile.objects.filter(user=self.user).exists())

    def test_staff_profile_update_via_user_save(self):
        """
        Check that saving the User calls save_profile, which saves the StaffProfile as well.
        """
        profile = self.user.profile
        profile.full_name = 'Profile User'
        profile.save()

        self.user.first_name = 'Profile'
        self.user.last_name = 'Tester'
        self.user.save()

        self.assertEqual(self.user.profile.full_name, 'Profile User')

    def test_staff_profile_str_method(self):
        """
        Ensure the StaffProfile's __str__ method uses the username.
        """
        profile_str = str(self.user.profile)
        expected_str = self.user.username
        self.assertEqual(profile_str, expected_str)

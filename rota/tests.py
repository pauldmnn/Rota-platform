from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rota.models import StaffProfile, Rota, Request

class RotaPlatformTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin', password='adminpass'
        )
        self.staff_user = User.objects.create_user(
            username='staff', password='staffpass'
        )
        self.profile = StaffProfile.objects.create(
            user=self.staff_user, full_name="Staff User"
        )

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'complexpassword',
            'password2': 'complexpassword',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'staff',
            'password': 'staffpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_rota_creation_by_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('create_rota'), {
            'user': self.staff_user.id,
            'date': '2024-12-30',
            'shift_type': 'Morning'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Rota.objects.filter(user=self.staff_user).exists())

    def test_day_off_request_submission(self):
        self.client.login(username='staff', password='staffpass')
        response = self.client.post(reverse('request_day_off'), {
            'date': '2024-12-31',
            'reason': 'Personal'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(DayOffRequest.objects.filter(user=self.staff_user).exists())


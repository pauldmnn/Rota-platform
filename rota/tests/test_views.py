import pytest
from django.test.utils import override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from rota.models import Rota

@pytest.mark.django_db
def test_home_view(client):
    """Ensure the home page loads successfully."""
    url = reverse('home')  
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_admin_login_view_invalid(client):
    url = reverse('admin_login')
    response = client.post(url, {'username': 'nonexistent', 'password': 'wrong'})
    assert response.status_code == 200
    messages = list(response.context['messages'])
    assert any("Invalid credentials" in message.message for message in messages)

@pytest.mark.django_db
def test_admin_login_view_valid(client):
    """A valid admin login should redirect to the appropriate admin page."""
    user = User.objects.create_user(username='adminuser', password='adminpass', is_staff=True)
    url = reverse('admin_login')
    response = client.post(url, {'username': 'adminuser', 'password': 'adminpass'})
    assert response.status_code == 302
    assert response.url in [reverse('admin_dashboard'), reverse('admin_create_rota')]

@pytest.mark.django_db
@override_settings(AXES_ENABLED=False)
def test_admin_create_rota_view_get(client):
    user = User.objects.create_user(username='adminuser', password='adminpass', is_staff=True)
    assert client.login(username='adminuser', password='adminpass')
    url = reverse('admin_create_rota')
    response = client.get(url)
    assert response.status_code == 200
    assert "Rota" in response.content.decode() 

@pytest.mark.django_db
@override_settings(AXES_ENABLED=False)
def test_admin_create_rota_view_post_valid(client):
    user = User.objects.create_user(username='adminuser', password='adminpass', is_staff=True, first_name='Admin', last_name='User')
    assert client.login(username='adminuser', password='adminpass')
    url = reverse('admin_create_rota')
    form_data = {
        'user': user.id,
        'date': '2025-04-22',
        'shift_type': 'Long Day',
        'start_time': '09:00',
        'end_time': '17:00'
    }
    response = client.post(url, form_data)
    assert response.status_code == 302

@pytest.mark.django_db
@override_settings(AXES_ENABLED=False)
def test_user_login_view_redirects(client):
    user = User.objects.create_user(username='regularuser', password='testpass')
    url = reverse('user_login')
    response = client.post(url, {'username': 'regularuser', 'password': 'testpass'})
    assert response.status_code == 302
    from django.urls import reverse as django_reverse
    assert response.url == django_reverse('staff_dashboard')

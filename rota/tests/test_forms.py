import pytest
from datetime import date
from django import forms
from django.contrib.auth.models import User
from rota.models import Rota
from rota.forms import RotaForm, RequestForm, SignupForm


@pytest.mark.django_db
def test_rota_form_creates_new_entry():
    """A valid RotaForm should create a new rota entry."""
    user = User.objects.create(username='testuser')
    form_data = {
        'user': user.id,
        'date': '2025-04-15',
        'shift_type': 'Long Day',
        'start_time': '08:00',
        'end_time': '16:00'
    }
    form = RotaForm(data=form_data)
    assert form.is_valid(), form.errors
    rota = form.save()
    assert rota.user == user
    assert rota.shift_type == 'Long Day'


@pytest.mark.django_db
def test_rota_form_validation_existing_shift():
    user = User.objects.create(username='testuser')
    Rota.objects.create(user=user, date=date(2025, 4, 15), shift_type='Long Day')
    form_data = {
        'user': user.id,
        'date': '2025-04-15',
        'shift_type': 'Long Day',
        'start_time': '08:00',
        'end_time': '16:00'
    }
    form = RotaForm(data=form_data)
    form.is_valid()  
    with pytest.raises(forms.ValidationError) as excinfo:
         form.save()
    assert "A shift has already been allocated for this date." in str(excinfo.value)


@pytest.mark.django_db
def test_request_form_valid():
    """Test that RequestForm accepts valid data."""
    form_data = {
        'date': '2025-04-20',
        'comment': 'Requesting day off'
    }
    form = RequestForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_signup_form_password_mismatch():
    """Test that SignupForm catches mismatched passwords."""
    form_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'differentpassword'
    }
    form = SignupForm(data=form_data)
    assert not form.is_valid()
    assert "Passwords do not match." in str(form.errors)

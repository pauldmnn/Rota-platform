import pytest
from datetime import date, time
from django.contrib.auth.models import User
from rota.models import Rota, Request, StaffProfile

@pytest.mark.django_db
def test_rota_str_custom():
    """Test the __str__ method for a custom shift in Rota."""
    user = User.objects.create(username='testuser', first_name='Test', last_name='User')
    rota = Rota.objects.create(
        user=user,
        date=date(2025, 4, 10),
        shift_type='Custom',
        start_time=time(9, 0),
        end_time=time(17, 0)
    )
    expected = f"{user.get_full_name()} - {rota.date} - Custom (09:00:00 to 17:00:00)"
    assert str(rota) == expected

@pytest.mark.django_db
def test_rota_str_default():
    """Test the __str__ method for a regular shift in Rota."""
    user = User.objects.create(username='testuser', first_name='Test', last_name='User')
    rota = Rota.objects.create(
        user=user,
        date=date(2025, 4, 10),
        shift_type='Long Day'
    )
    expected = f"{user.get_full_name()} - {rota.date} - Long Day"
    assert str(rota) == expected

@pytest.mark.django_db
def test_request_str():
    """Test the __str__ method of Request model."""
    user = User.objects.create(username='testuser')
    req = Request.objects.create(
        user=user,
        date=date(2025, 4, 11),
        comment="Test request",
        status="Pending"
    )
    expected = f"{user.username} - {req.date} (Pending)"
    assert str(req) == expected


@pytest.mark.django_db
def test_staffprofile_str():
    """Test the __str__ method of StaffProfile using the auto-created profile."""
    user = User.objects.create(username='testuser')
    
    profile = user.profile
    profile.full_name = 'Test User'
    profile.address = '123 Test St'
    profile.email = 'test@example.com'
    profile.save()
    
    assert str(profile) == 'testuser'

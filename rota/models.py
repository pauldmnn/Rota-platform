from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


SHIFT_CHOICES = [
    ("Long Day", "Long Day"),
    ("Early", "Early"),
    ("Late", "Late"),
    ("Night", "Night"),
    ("Custom", "Custom"),
    ("Requested Off", "Requested Off"),
    ("Sickness/Absence", "Sickness/Absence"),
]


class Rota(models.Model):
    """
    Model to store shift details for staff members.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    shift_type = models.CharField(
        max_length=50, choices=SHIFT_CHOICES, default="Long Day"
    )
    sickness_or_absence_type = models.CharField(max_length=255,
                                                blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        if self.shift_type == "Custom" and self.start_time and self.end_time:
            return (
                f"{self.user.get_full_name()} - {self.date} - Custom "
                f"({self.start_time} to {self.end_time})"
            )
        return f"{self.user.get_full_name()} - {self.date} - {self.shift_type}"


class Request(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='requests')
    date = models.DateField()
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='Pending')
    admin_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.status})"


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    full_name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True,
                              null=True, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically create a StaffProfile only if one doesn't already exist.
    """
    if created:
        StaffProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Automatically save the StaffProfile when the User is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()

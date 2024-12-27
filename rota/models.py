from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

# Shift Type Choices
SHIFT_CHOICES = [
    ("Long Day", "Long Day"),
    ("Early", "Early"),
    ("Late", "Late"),
    ("Night", "Night"),
    ("Custom", "Custom"),
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
    sickness_or_absence_type = models.CharField(max_length=255, blank=True, null=True)  # New field
    start_time = models.TimeField(blank=True, null=True)  
    end_time = models.TimeField(blank=True, null=True) 
    is_updated = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'date')


    def __str__(self):
        if self.shift_type == "Custom" and self.start_time and self.end_time:
            return f"{self.user} - {self.date} - Custom ({self.start_time} to {self.end_time})"
        return f"{self.user} - {self.date} - {self.shift_type}"

# Staff making request to be off or work certain days
class Request(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    date = models.DateField()  # Ensure this field is present
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    admin_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.user} - {self.date} ({self.status})"


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)  # New field for job title

    def __str__(self):
        return self.full_name

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


@receiver(post_save, sender=Rota)
def send_rota_notification(sender, instance, created, **kwargs):
    """
    Sends an email notification to the user when a rota is created.
    """
    if created:
        user = instance.user
        subject = "Your New Rota Assignment"
        message = (
            f"Hello {user.get_full_name()},\n\n"
            f"You have been assigned a new shift:\n"
            f"Date: {instance.date}\n"
            f"Shift Type: {instance.shift_type}\n\n"
            "Please log in to the platform for more details.\n"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
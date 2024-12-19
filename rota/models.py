from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver

# Shift Type Choices
SHIFT_CHOICES = [
    ("Long Day", "Long Day"),
    ("Early", "Early"),
    ("Late", "Late"),
    ("Night", "Night"),
    ("Custom", "Custom"),
]


class Rota(models.Model):
    """
    Model to store shift details for staff members.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    date = models.DateField()  
    shift_type = models.CharField(
        max_length=20, choices=SHIFT_CHOICES, default="Long Day"
    )  
    start_time = models.TimeField(blank=True, null=True)  
    end_time = models.TimeField(blank=True, null=True) 
    is_updated = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'date')


    def __str__(self):
        if self.shift_type == "Custom" and self.start_time and self.end_time:
            return f"{self.user.username} - {self.date} - Custom ({self.start_time} to {self.end_time})"
        return f"{self.user.username} - {self.date} - {self.shift_type}"

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
        return f"{self.user.username} - {self.date} ({self.status})"


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        StaffProfile.objects.create(user=instance)

# Automatically save the StaffProfile when the User is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
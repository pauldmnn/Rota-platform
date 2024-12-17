from django.db import models
from django.contrib.auth.models import User
from datetime import date

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Staff member
    date = models.DateField()  # Date of the shift
    shift_type = models.CharField(
        max_length=20, choices=SHIFT_CHOICES, default="Long Day"
    )  # Type of shift
    start_time = models.TimeField(blank=True, null=True)  # Optional start time for custom shifts
    end_time = models.TimeField(blank=True, null=True)  # Optional end time for custom shifts

    class Meta:
        unique_together = ('user', 'date')


    def __str__(self):
        if self.shift_type == "Custom" and self.start_time and self.end_time:
            return f"{self.user.username} - {self.date} - Custom ({self.start_time} to {self.end_time})"
        return f"{self.user.username} - {self.date} - {self.shift_type}"


class Request(models.Model):
    """
    Model for staff day-off requests.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Staff member making the request
    requested_day = models.DateField()  # Day they are requesting off
    comment = models.TextField(blank=True, null=True)  # Staff comment for the request
    status = models.CharField(
        max_length=10,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending",
    )  # Status of the request
    admin_comment = models.TextField(blank=True, null=True)  # Admin's reason for rejection

    def __str__(self):
        return f"{self.user.username} - {self.requested_day} ({self.status})"

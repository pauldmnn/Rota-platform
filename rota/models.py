from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Shift type choices
SHIFT_CHOICES = [
    ("Long Day", "Long Day"),
    ("Early", "Early"),
    ("Late", "Late"),
    ("Night", "Night"),
    ("Custom", "Custom"),
]

class Rota(models.Model):
    """
    Rota model represents the work schedule for staff.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    date = models.DateField(default=date(2024, 1, 1))  # The specific date for the rota
    shift_type = models.CharField(max_length=10, choices=SHIFT_CHOICES, default="Long Day")  # Shift type
    start_time = models.TimeField(blank=True, null=True)  # Optional custom start time
    end_time = models.TimeField(blank=True, null=True)  # Optional custom end time

    @property
    def day(self):
        """
        Automatically calculate the day of the week based on the date.
        """
        return self.date.strftime("%A")  # e.g., Monday, Tuesday

    def __str__(self):
        if self.shift_type == "Custom" and self.start_time and self.end_time:
            return f"{self.user.username}: {self.date} - {self.shift_type} ({self.start_time} to {self.end_time})"
        return f"{self.user.username}: {self.date} - {self.shift_type}"


class Request(models.Model):
    """
    Request model allows staff to request specific days to work.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    requested_day = models.DateField()  # Date requested by the user
    status = models.CharField(max_length=10, choices=[
            ("Pending", "Pending"),
            ("Approved", "Approved"),
            ("Refused", "Refused"),
        ], default="Pending"
    )  # Status of the request
    comment = models.TextField(blank=True, null=True)  # Admin comment (e.g., reason for refusal)

    def __str__(self):
        return f"{self.user.username}: {self.requested_day} ({self.status})"

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
    """
    Model for staff day-off requests.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    requested_day = models.DateField() 
    comment = models.TextField(blank=True, null=True)  
    status = models.CharField(
        max_length=10,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending",
    )  
    admin_comment = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"{self.user.username} - {self.requested_day} ({self.status})"

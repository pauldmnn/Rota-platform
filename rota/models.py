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
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    date = models.DateField()
    comment = models.TextField(blank=True, null=True)  # Staff-provided comment
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    admin_comment = models.TextField(blank=True, null=True)  # Admin response/comment
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.status})"


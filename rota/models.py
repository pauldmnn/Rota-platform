from django.db import models
from django.contrib.auth.models import User
# Create your models here.

SHIFT_CHOICES = [
    ("Long Day", "Long Day"),
    ("Early", "Early"),
    ("Late", "Late"),
    ("Night", "Night"),
    ("Custom", "Custom")
]


class Rota(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=[
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ])
    shift_type = models.CharField(max_length=10, choices=SHIFT_CHOICES, default="Long Day")
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}: {self.day} - {self.shift_type}"


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_day = models.CharField(max_length=10, choices=[
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ])
    status = models.CharField(max_length=10, choices=[
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Refused", "Refused"),
    ], default="Pending")
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}: {self.requested_day} ({self.status})"
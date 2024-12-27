from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Rota

@receiver(post_save, sender=Rota)
def send_rota_notification(sender, instance, created, **kwargs):
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

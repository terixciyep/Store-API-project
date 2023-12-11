from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_mail_for_verify
from users.models import UserModel



@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        send_mail_for_verify(user=instance)

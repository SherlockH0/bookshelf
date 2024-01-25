from django.db.models.signals import post_save
from .models import User, Customer
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

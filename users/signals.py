from django.contrib.auth.models import User
from users.models import Cart
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user_id=instance)


# @receiver(post_save, sender=User)
# def save_cart(sender, instance, created, **kwargs):
#     instance.

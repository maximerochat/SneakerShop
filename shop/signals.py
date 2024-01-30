from .models import Option, Shoes
from django.db.models.signals import post_save
from django.dispatch import receiver


# @receiver(post_save, sender=Option)
# def create_cart(sender, instance, created, **kwargs):
#     if created:
#         Shoes.CHOICES = {"vide": 1}         #update_choices(instance.option, instance.option)
#         print(Shoes.CHOICES)

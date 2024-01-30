from django.db import models
from shop.models import Shoes
from django.contrib.auth.models import User
# Create your models here.

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Shoes)
    quantity = models.JSONField(default=dict())

    @property
    def sum(self):
        return sum(item.price * self.quantity[str(item.auto_increment_id)] for item in self.items.all())

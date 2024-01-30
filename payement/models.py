from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.AutoField(primary_key=True)
    items = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id}"

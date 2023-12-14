from django.contrib.auth import get_user_model
from django.db import models

from items.models import Item


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ManyToManyField(Item)

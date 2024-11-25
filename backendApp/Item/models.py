from django.db import models

from backendApp import Attribute
from backendApp.Type.models import Type


class Item(models.Model):
    name = models.CharField(max_length=60, unique=True)
    amount = models.IntegerField()
    room_with_items = models.ForeignKey(
        'RoomWithItems.RoomWithItems', on_delete=models.CASCADE, related_name='items', null=False, unique=True
    )
    type = models.ForeignKey(
        'Type.Type', on_delete=models.CASCADE, related_name='items', null=False
    )
    attribute = models.ForeignKey(
        'Attribute.Attribute' , on_delete=models.CASCADE, related_name='items', null=True
    )

    def __str__(self):
        return self.name
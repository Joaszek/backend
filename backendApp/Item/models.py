from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=60)
    amount = models.IntegerField()
    room_with_items = models.ForeignKey(
        'RoomWithItems.RoomWithItems', on_delete=models.CASCADE, related_name='items'
    )

    def __str__(self):
        return self.name

from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=60, unique=True)
    amount = models.IntegerField()
    room_with_items = models.ForeignKey(
        'RoomWithItems.RoomWithItems', on_delete=models.CASCADE, related_name='items'
    )
    type = models.CharField(max_length=100)
    attribute = models.CharField(max_length=100, default="Unknown")

    def __str__(self):
        return self.name

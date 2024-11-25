from django.db import models


class RoomWithItems(models.Model):
    id = models.AutoField(primary_key=True)
    room_number = models.IntegerField()
    is_to_rent = models.BooleanField(default=False, editable=False, blank=True)
    building = models.ForeignKey(
        'Building.Building', on_delete=models.CASCADE, related_name='rooms_with_items', null=False
    )

    class Meta:
        unique_together = ('room_number', 'building')  # Ograniczenie unikalności

    def __str__(self):
        return f"Room {self.room_number} in {self.building.name}"

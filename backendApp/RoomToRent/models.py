from django.db import models


class RoomToRent(models.Model):
    room_number = models.IntegerField()
    building = models.ForeignKey(
        'Building.Building', on_delete=models.CASCADE, related_name='rooms_to_rent'
    )

    def __str__(self):
        return f"Room {self.room_number} in {self.building.name}"

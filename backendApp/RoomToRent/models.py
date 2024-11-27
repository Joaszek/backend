from django.db import models


class RoomToRent(models.Model):
    room_to_rent_id = models.CharField(max_length=100, unique=False, default='Unknown')
    room_number = models.IntegerField()
    is_to_rent = models.BooleanField(default=True, editable=False, blank=True)
    building = models.CharField(max_length=100, unique=False, default='Unknown')
    faculty = models.CharField(max_length=100, unique=False, default='Unknown')
    class Meta:
        unique_together = ('room_number', 'building')  # Ograniczenie unikalności

    def __str__(self):
        return f"Room {self.room_number} in {self.building}"

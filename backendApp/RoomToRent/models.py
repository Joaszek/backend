from django.db import models


class RoomToRent(models.Model):
    id = models.AutoField(primary_key=True)
    room_number = models.IntegerField()
    is_to_rent = models.BooleanField(default=True, editable=False, blank=True)
    building = models.CharField(max_length=100, unique=False, default='Unknown')
    faculty = models.CharField(max_length=100, unique=False, default='Unknown')
    available = models.BooleanField(default=True, unique=False)
    
    class Meta:
        unique_together = ('room_number', 'building')  # Ograniczenie unikalności

    def __str__(self):
        return f"Room {self.room_number} in {self.building}"

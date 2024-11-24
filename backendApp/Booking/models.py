from django.db import models
from django.conf import settings


class Booking(models.Model):
    room_to_rent = models.OneToOneField(
        'RoomToRent.RoomToRent', on_delete=models.CASCADE, related_name='bookings'
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings'
    )
    start_time = models.DateField()
    end_time = models.DateField()

    def __str__(self):
        return f"Booking by {self.user} for {self.room_to_rent}"

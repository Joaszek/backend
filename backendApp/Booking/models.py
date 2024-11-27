from django.db import models
from django.conf import settings


class Booking(models.Model):

    booking_id = models.CharField(max_length=100, unique=False, default='Unknown')
    item_id = models.CharField(max_length=100, unique=False, default='Unknown')
    item_name = models.CharField(max_length=100, unique=False, default='Unknown')
    room_id = models.CharField(max_length=100, unique=False, default='Unknown')
    user = models.CharField(max_length=100, unique=False, default='Unknown')
    start_time = models.DateField()
    end_time = models.DateField()
    building = models.CharField(max_length=100, unique=False, default='Unknown')
    faculty = models.CharField(max_length=100, unique=False, default='Unknown')
    isRoomToRent = models.BooleanField(default=True, unique=False)

    def __str__(self):
        return f"Booking by {self.user} for {self.booking_id}"

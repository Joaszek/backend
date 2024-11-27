from django.db import models
from django.conf import settings


class ItemBooking(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_id = models.CharField(max_length=100, unique=False, default='Unknown')
    student_id = models.CharField(max_length=100, unique=False, default='Unknown')
    start_date = models.CharField(max_length=100, unique=False, default='Unknown')
    end_date = models.CharField(max_length=100, unique=False, default='Unknown')
    def __str__(self):
        return f"Item {self.id} booked by {self.student_id}"

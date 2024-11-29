from django.db import models


class ItemBooking(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=False, default='Unknown')
    item_id = models.CharField(max_length=100, unique=False, default='Unknown')
    student_id = models.CharField(max_length=100, unique=False, default='Unknown')
    start_date = models.CharField(max_length=100, unique=False, default='Unknown')
    end_date = models.CharField(max_length=100, unique=False, default='Unknown')
    returned = models.BooleanField(default=False, unique=False)

    def __str__(self):
        return f"Item {self.id} booked by {self.student_id}"

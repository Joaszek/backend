from django.db import models
from django.conf import settings


class ItemBooking(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(
        'Item.Item', on_delete=models.CASCADE, related_name='item_bookings'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='item_bookings'
    )
    start_date = models.DateField(null=False)
    end_date = models.DateField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"Item {self.item.name} booked by {self.user}"

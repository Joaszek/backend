from django.db import models

class Item(models.Model):
    item_id = models.CharField(max_length=100, unique=False, default='Unknown')
    name = models.CharField(max_length=60, unique=True)
    amount = models.IntegerField()
    room_with_items = models.CharField(max_length=100, unique=False, default='Unknown')
    type = models.CharField(max_length=100, default="Unknown")
    attribute = models.CharField(max_length=100, default="Unknown")
    user = models.CharField(max_length=100, unique=False, default="Unknown")
    start_date = models.CharField(max_length=100, unique=False, default="Unknown")
    end_date = models.CharField(max_length=100, unique=False, default="Unknown")
    faculty = models.CharField(max_length=100, unique=False, default="Unknown")
    building = models.CharField(max_length=100, unique=False, default="Unknown")


    def __str__(self):
        return self.name

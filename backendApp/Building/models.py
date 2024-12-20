from django.db import models


class Building(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, unique=True)
    faculty = models.CharField(max_length=50, unique=False, default="Unknown")

    def __str__(self):
        return self.name

# backendApp/Admin/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser


class Admin(AbstractUser):
    admin_field = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

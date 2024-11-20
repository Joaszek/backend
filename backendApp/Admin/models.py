from django.contrib.auth.models import AbstractUser
from django.db import models


class Admin(AbstractUser):
    additional_field = models.CharField(max_length=255, blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='admin_user_groups',  # Unique related_name for Admin groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='admin_user_permissions',  # Unique related_name for Admin permissions
        blank=True
    )

    def __str__(self):
        return self.username

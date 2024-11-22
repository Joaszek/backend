from django.contrib.auth.models import AbstractUser
from django.db import models


class Student(AbstractUser):
    id = models.AutoField(primary_key=True)
    additional_field = models.CharField(max_length=255, blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='student_user_groups',  # Unique related_name for Student groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='student_user_permissions',  # Unique related_name for Student permissions
        blank=True
    )

    def __str__(self):
        return self.username

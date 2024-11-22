from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    additional_field = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True, default="Adam")
    last_name = models.CharField(max_length=255, blank=True, null=True, default="Kowalski")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    def set_password(self, raw_password):
        """
        Hash and set the password.
        """
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Check if the provided password matches the stored hashed password.
        """
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

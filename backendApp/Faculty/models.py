from django.db import models

class Faculty(models.Model):
    faculty_id = models.CharField(max_length=100, unique=False, default='Unknown')
    name = models.CharField(max_length=255, unique=True)
    admin_id = models.CharField(max_length=100, unique=False, default='Unknown')

    def __str__(self):
        return self.name

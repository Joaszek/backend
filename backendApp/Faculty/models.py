from django.db import models


class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    admin = models.ForeignKey(
        'Admin.Admin', on_delete=models.CASCADE, related_name='faculties'
    )

    def __str__(self):
        return self.name

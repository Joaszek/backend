from django.db import models


class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    admin = models.ForeignKey(
        'Admin.Admin', on_delete=models.CASCADE, related_name='faculties'
    )
    building = models.ForeignKey(
        'Building.Building', on_delete=models.CASCADE, related_name='faculties', null=True, blank=True
    )

    def __str__(self):
        return self.name

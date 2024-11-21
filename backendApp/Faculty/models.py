from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(
        'Admin.Admin', on_delete=models.CASCADE, related_name='faculties'
    )
    building = models.ForeignKey(
        'Building.Building', on_delete=models.CASCADE, related_name='faculties'
    )

    def __str__(self):
        return self.name

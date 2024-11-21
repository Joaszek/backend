from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=10)
    faculty = models.ForeignKey(
        'Faculty.Faculty', on_delete=models.CASCADE, related_name='buildings'
    )

    def __str__(self):
        return self.name

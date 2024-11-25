from django.db import models


class Building(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, unique=True)
    faculty = models.ForeignKey(
        'Faculty.Faculty', on_delete=models.CASCADE, related_name='buildings', null=False
    )

    def __str__(self):
        return self.name

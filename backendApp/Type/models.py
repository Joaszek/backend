from django.db import models

# Create your models here.
class Type(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.type_name
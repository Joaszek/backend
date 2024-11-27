from django.db import models

# Create your models here.
class Attribute(models.Model):
    id = models.AutoField(primary_key=True)
    attribute_name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.attribute_name
from django.db import models

# Create your models here.
class tuanju(models.Model):
    name = models.CharField(max_length =64)
    icon = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    tuanju_type = models.CharField(max_length = 64)
    order = models.IntegerField(default=0)

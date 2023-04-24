from django.db import models
from django.conf import settings

# Create your models here.

class Fox(models.Model):
    name = models.CharField(max_length=32)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
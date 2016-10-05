from __future__ import unicode_literals

from django.db import models
from geoposition.fields import GeopositionField

# Create your models here.
from users.models import SIAUser

class Location(models.Model):
    user = models.ForeignKey(SIAUser)
    name = models.CharField(max_length=100)
    position = GeopositionField()

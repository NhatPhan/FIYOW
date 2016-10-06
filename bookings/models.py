from __future__ import unicode_literals

from django.db import models
from users.models import SIAUser

# Create your models here.

class Flight(models.Model):
    """
    Representation of a flight
    """
    user = models.ForeignKey(SIAUser)
    from_airport = models.CharField(max_length=200, null=True)
    to_airport = models.CharField(max_length=200, null=True)
    departure_time = models.DateTimeField(null=True)
    arrival_time = models.DateTimeField(null=True)
    price = models.DecimalField(null=True)
    
class AttractionTicket(models.Model):
    """
    Representation of a attraction
    """
    user = models.ForeignKey(SIAUser)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.DecimalField(null=True)
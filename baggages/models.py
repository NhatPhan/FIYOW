from __future__ import unicode_literals

from django.db import models
from bookings.models import Booking

# Create your models here.
class Baggage(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    weight = models.FloatField(null=True)
    color = models.CharField(null=True, max_length=20)
    status = models.CharField(null=True, max_length=250)
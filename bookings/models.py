from __future__ import unicode_literals

from django.db import models
from users.models import SIAUser

# Create your models here.

class Booking(models.Model):
    """
    Representation of a flight
    """
    user = models.ForeignKey(SIAUser, null=True)
    from_airport = models.CharField(max_length=200, null=True)
    to_airport = models.CharField(max_length=200, null=True)
    departure_time = models.DateTimeField(null=True)
    arrival_time = models.DateTimeField(null=True)
    price = models.FloatField(null=True)

    class Meta:
        ordering = ['departure_time']

    def as_json(self):
        return dict(
            user_id=self.user.id, from_airport=self.from_airport,
            to_airport=self.to_airport,
            departure_time=self.departure_time,
            arrival_time=self.arrival_time,
            price=self.price)


class AttractionTicket(models.Model):
    """
    Representation of a attraction
    """
    user = models.ForeignKey(SIAUser, null=True)
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)


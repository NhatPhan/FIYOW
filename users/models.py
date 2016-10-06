from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class SIAUser(models.Model):
    """
    Representation of a client
    """

    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    postal_address = models.CharField(max_length=500, null=True)
    residence_country = models.CharField(max_length=200, null=True)
    nationality = models.CharField(max_length=200, null=True)
    dob = models.DateField(null=True, verbose_name="Date of birth")
    language = models.CharField(null=True, max_length=200)
    
    #Credit Card Info
    name_on_card = models.CharField(max_length=200, null=True)
    card_number = models.CharField(max_length=20, null=True)
    expiration_month = models.IntegerField(null=True)
    expiration_year = models.IntegerField(null=True)
    cvv_number = models.IntegerField(null=True)


    @classmethod
    def create(cls, user, first_name, last_name, postal_address=None, residence_country=None, nationality=None, dob=None):
        SIAUser = cls(user=user, first_name=first_name, last_name=last_name,
                postal_address=postal_address, residence_country=residence_country,
                 nationality=nationality, dob=dob)
        return SIAUser

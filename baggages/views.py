from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests, json
from string import Template
from datetime import datetime
from json import dumps
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

# assuming obj is a model instance

from bookings.models import Booking
from users.models import SIAUser

@api_view(['GET'])
def baggageStatus(request):
    data = request.query_params
    print(data)
    first_name = data['first_name']
    last_name = data['last_name']

    user = SIAUser.objects.get(first_name=first_name, last_name=last_name)
    baggages = Booking.objects\
        .filter(user=user,
                departure_time__gte=datetime.today())[0].baggage_set.all()
    print(baggages)
    response = serializers.serialize('json', list(baggages))

    print(response)

    return Response(response)
    


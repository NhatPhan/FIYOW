from django.shortcuts import render

from rest_framework.response import Response

import requests, json
from datetime import datetime
from django.core import serializers

from bookings.models import Booking
from baggages.models import Baggage
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer

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
    
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def addBaggageForBooking(request):
    # Handling flight search
    if request.method == 'POST':
        booking_data = request.data
        booking_id = booking_data['booking_id']
        weight = booking_data['weight']
        color = booking_data['color']
        status = booking_data['status']

        booking = Booking.objects.get(id=booking_id)
        baggage = Baggage(booking=booking, weight=weight, color=color, status=status)
        baggage.save()
        response = {"sticker": "One baggage has been added for the booking with id: ",
                         "booking_id": booking_id}
        return Response(response, template_name='bookings/baggage-add.html')

    # Search form
    else:
        return render(request, 'bookings/baggage-add.html')

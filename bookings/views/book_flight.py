import json
import demjson
from string import Template

import requests

from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from bookings.models import Booking
from users.models import SIAUser
from django.core import serializers

@api_view(['POST', 'GET'])
@renderer_classes([TemplateHTMLRenderer])
def book_flight(request):
    # Handling flight search
    if request.method == 'POST':
        user = SIAUser.objects.get(user__id=request.user.id)
        data = request.data['json_segment']
        total_price = request.data['price']
        currency = request.data['currency']
        data = data.replace("u\'", "\'").replace("\'", "\"").replace("True", "\"True\"").replace("False", "\"False\"")
        json_data = json.loads(data)
        segments = json_data['segments']
        num_segments = len(segments)
        price_per_segment = float(total_price) / num_segments
        bookings = []
        for segment in segments:
            from_ = segment['departureAirportLocation']
            to_ = segment['arrivalAirportLocation']
            dep_time = segment['departureTimeRaw']
            arr_time = segment['arrivalTimeRaw']
            booking = Booking(user=user, from_airport=from_, to_airport=to_,
                              departure_time=dep_time , arrival_time=arr_time , price=price_per_segment)
            booking.save()
            bookings.append(booking.as_json())
        response = {'bookings': bookings, 'currency': currency}
        return Response(response, template_name='bookings/booking_result.html')


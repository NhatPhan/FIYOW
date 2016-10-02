import json
from string import Template

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def hotel_offers(request):
    """
    hotelId (required)
    priceType
    sourceType (mobileweb or mobileapp)
    checkInDate (require, ISO format)
    checkOutDate (require, ISO format)
    room1
    room (same as 3.4.1)
    """

    hotel_data = request.data
    hotel_id = 'hotelId=' + hotel_data['hotelId'] + '&' if 'hotelId' in hotel_data.keys() else ''
    price_type = 'priceType=' + hotel_data['priceType'] + '&' if 'priceType' in hotel_data.keys() else ''
    source_type = 'sourceType=' + hotel_data['sourceType'] + '&' if 'sourceType' in hotel_data.keys() else ''
    check_in_date = 'checkInDate=' + hotel_data['checkInDate'] + '&' if 'checkInDate' in hotel_data.keys() else ''
    check_out_date = 'checkOutDate=' + hotel_data['checkOutDate'] + '&' if 'checkOutDate' in hotel_data.keys() else ''
    room1 = 'room1=' + hotel_data['room1'] + '&' if 'room1' in hotel_data.keys() else ''
    room = 'room=' + hotel_data['room'] + '&' if 'room' in hotel_data.keys() else ''

    s = Template('http://terminal2.expedia.com:80/x/mhotels/offers?$hotelId$priceType$sourceType$checkInDate$checkOutDate$room1$room')
    search = s.substitute(hotelId=hotel_id,
            priceType=price_type,
            sourceType=source_type,
            checkInDate=check_in_date,
            checkOutDate=check_out_date,
            room1=room1,
            room=room) + 'apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'
    response = requests.get(search)
    content = json.loads(response.content)
    return Response(content, status=response.status_code)

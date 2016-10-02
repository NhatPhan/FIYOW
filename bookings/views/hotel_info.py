import json
from string import Template

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def hotel_info(request):
    """
    hotelId (required)
    """

    hotel_data = request.data
    hotel_id = 'hotelId=' + hotel_data['hotelId'] + '&' if 'hotelId' in hotel_data.keys() else ''

    s = Template('http://terminal2.expedia.com:80/x/mhotels/info?$hotelId')
    search = s.substitute(hotelId=hotel_id) + 'apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'
    response = requests.get(search)
    content = json.loads(response.content)
    return Response(content, status=response.status_code)

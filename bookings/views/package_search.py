import json
from string import Template

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def package_search(request):
    """
    originAirport (required)
    destinationAirport (required)
    departureDate (required)
    returnDate (required)
    regionid
    hotelids
    adults
    childages
    infantinseat (boolean)
    limit
    class (coach, first, business, premium coach)
    nonstop (boolean, true=> nonstop flight only)
    """

    package_data = request.data
    origin_airport = 'originAirport=' + package_data['originAirport'] + '&' if 'originAirport' in package_data.keys() else ''
    destination_airport = 'destinationAirport=' + package_data['destinationAirport'] + '&' if 'destinationAirport' in package_data.keys() else ''
    departure_date = 'departureDate=' + package_data['departureDate'] + '&' if 'departureDate' in package_data.keys() else ''
    return_date = 'returnDate=' + package_data['returnDate'] + '&' if 'returnDate' in package_data.keys() else ''
    region_id = 'regionid=' + package_data['regionid'] + '&' if 'regionid' in package_data.keys() else ''
    hotel_ids = 'hotelids=' + package_data['hotelids'] + '&' if 'hotelids' in package_data.keys() else ''
    adults = 'adults=' + package_data['adults'] + '&' if 'adults' in package_data.keys() else ''
    child_ages = 'childages=' + package_data['childages'] + '&' if 'childages' in package_data.keys() else ''
    infant_in_seat = 'infantinseat=' + package_data['infantinseat'] + '&' if 'infantinseat' in package_data.keys() else ''
    limit = 'limit=' + package_data['limit'] + '&' if 'limit' in package_data.keys() else ''
    class_ = 'class=' + package_data['class'] + '&' if 'class' in package_data.keys() else ''
    nonstop = 'nonstop=' + package_data['nonstop'] + '&' if 'nonstop' in package_data.keys() else ''

    s = Template('http://terminal2.expedia.com:80/x/packages?$originAirport$destinationAirport$departureDate$returnDate$regionid$hotelids$adults$childages$infantinseat$limit$class_$nonstop')
    search = s.substitute(originAirport=origin_airport,
            destinationAirport=destination_airport,
            departureDate=departure_date,
            returnDate=return_date,
            regionid=region_id,
            hotelids=hotel_ids,
            adults=adults,
            childages=child_ages,
            infantinseat=infant_in_seat,
            limit=limit,
            class_=class_,
            nonstop=nonstop) + 'apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'
    response = requests.get(search)
    content = json.loads(response.content)
    return Response(content, status=response.status_code)


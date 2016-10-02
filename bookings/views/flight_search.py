import json
from string import Template

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def flight_search(request):
    """
    departureDate(required)
    returnDate
    departureAirport(required)
    returnAirpot(required)
    numberOfAdultParameters
    childTravelerAge
    infantSeatingInLap
    correlationId
    maxOfferCount
    """

    flight_data = request.data
    departure_airport = 'departureAirport=' + flight_data['departureAirport'] + '&' if 'departureAirport' in flight_data.keys() else ''
    arrival_airport = 'arrivalAirport=' + flight_data['arrivalAirport'] + '&' if 'arrivalAirport' in flight_data.keys() else ''
    departure_date = 'departureDate=' + flight_data['departureDate'] + '&' if 'departureDate' in flight_data.keys() else ''
    return_date = 'returnDate=' + flight_data['returnDate'] + '&' if 'returnDate' in flight_data.keys() else ''
    number_of_adult_travellers = 'numberOfAdultTravellers=' + flight_data['numberOfAdultTravellers'] + '&' if 'numberOfAdultTravellers' in flight_data.keys() else ''
    child_traveler_age = 'childTravelerAge=' + flight_data['childTravelerAge'] + '&' if 'childTravelerAge' in flight_data.keys() else ''
    infant_seating_in_lap = 'infantSeatingInLap=' + flight_data['infantSeatingInLap'] + '&' if 'infantSeatingInLap' in flight_data.keys() else ''
    correlation_id = 'correlationId=' + flight_data['correlationId'] + '&' if 'correlationId' in flight_data.keys() else ''
    max_offer_count = 'maxOfferCount=' + flight_data['maxOfferCount'] + '&' if 'maxOfferCount' in flight_data.keys() else ''
    s = Template('http://terminal2.expedia.com/x/mflights/search?$departureAirport$arrivalAirport$departureDate$returnDate$numberOfAdultTravellers$childTravelerAge$infantSeatingInLap$correlationId$maxOfferCount')
    search = s.substitute(departureAirport=departure_airport,
        arrivalAirport=arrival_airport,
        departureDate=departure_date,
        returnDate=return_date,
        numberOfAdultTravellers=number_of_adult_travellers,
        childTravelerAge=child_traveler_age,
        infantSeatingInLap=infant_seating_in_lap,
        correlationId=correlation_id,
        maxOfferCount=max_offer_count) + 'prettyPrint=true&apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'
    response = requests.get(search)
    content = json.loads(response.content)
    return Response(content, status=response.status_code)
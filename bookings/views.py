from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests, json
from string import Template

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


@api_view(['POST'])
def flight_overview(request):
    flight_data = request.data
    start_date = flight_data['startDate'] if 'startDate' in flight_data.keys() else ''
    day_count = int(flight_data['dayCount']) if 'dayCount' in flight_data.keys() else 10
    origin = flight_data['origin'] if 'origin' in flight_data.keys() else ''
    destination = flight_data['destination'] if 'destination' in flight_data.keys() else ''
    
    post_data = {
        "MessageHeader": { "ClientInfo": { "DirectClientName": "Hackathon"}, "TransactionGUID": ""},
        "tpid": 1, "eapid": 0, 
        "PointOfSaleKey": { "JurisdictionCountryCode": "USA", "CompanyCode": "10111", "ManagementUnitCode": "1010" },
        
        "OriginAirportCodeList": {
            "AirportCode": [origin]
        },
        "DestinationAirportCodeList": {
            "AirportCode": [destination]
        }
    }
    
    if start_date != "" and day_count > 0: # checking dayCount to avoid user setting dayCount to 0 or negative number on purpose
        post_data["FareCalendar"] = {
            "StartDate" : start_date,
            "DayCount" : day_count
        }
        
        
    custom_headers = { 'Accept-Charset': 'UTF-8',
            'CONTENT-TYPE' : 'application/json',
            'Accept' : 'application/json'}

    response = requests.post('http://terminal2.expedia.com:80/x/flights/overview/get?apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44', 
        data=json.dumps(post_data),
        headers=custom_headers)
    content = json.loads(response.content)
    return Response(content, status=response.status_code)

@api_view(['POST'])
def car_search(request):
    """
    pickupdate
    dropoffdate
    pickuplocation
    dropofflocation
    sort
    limit
    suppliers
    classes
    """
    
    
    flight_data = request.data
    pickup_date = 'pickupdate=' + flight_data['pickupdate'] + '&' if 'pickupdate' in flight_data.keys() else ''
    drop_off_date = 'dropoffdate=' + flight_data['dropoffdate'] + '&' if 'dropoffdate' in flight_data.keys() else ''
    pickup_location = 'pickuplocation=' + flight_data['pickuplocation'] + '&' if 'pickuplocation' in flight_data.keys() else ''
    dropoff_location = 'dropofflocation=' + flight_data['dropofflocation'] + '&' if 'dropofflocation' in flight_data.keys() else ''
    sort = 'sort=' + flight_data['sort'] + '&' if 'sort' in flight_data.keys() else ''
    limit = 'limit=' + flight_data['limit'] + '&' if 'limit' in flight_data.keys() and flight_data['limit'] > 0 else 10
    suppliers = 'suppliers=' + flight_data['suppliers'] + '&' if 'suppliers' in flight_data.keys() else ''
    classes = 'classes=' + flight_data['classes'] + '&' if 'classes' in flight_data.keys() else ''
    
    s = Template("http://terminal2.expedia.com:80/x/cars/search?$pickupdate$dropoffdate$pickuplocation$dropofflocation$sort$limit$suppliers$classes")
    
    search = s.substitute(pickupdate=pickup_date,
        dropoffdate=drop_off_date,
        pickuplocation=pickup_location,
        dropofflocation=dropoff_location,
        sort=sort,
        limit=limit,
        suppliers=suppliers,
        classes=classes) + 'apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'

    response = requests.get(search)
    content = json.loads(response.content)
    return Response(content, status=response.status_code)

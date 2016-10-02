from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests, json
from string import Template

@api_view(['POST'])
def flightSearch(request):
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

    flightData = request.data
    departureAirport = 'departureAirport=' + flightData['departureAirport'] + '&' if 'departureAirport' in flightData.keys() else ''
    arrivalAirport = 'arrivalAirport=' + flightData['arrivalAirport'] + '&' if 'arrivalAirport' in flightData.keys() else '' 
    departureDate = 'departureDate=' + flightData['departureDate'] + '&' if 'departureDate' in flightData.keys() else '' 
    returnDate = 'returnDate=' + flightData['returnDate'] + '&' if 'returnDate' in flightData.keys() else ''
    numberOfAdultParameters = 'numberOfAdultParameters=' + flightData['numberOfAdultParameters'] + '&' if 'numberOfAdultParameters' in flightData.keys() else ''
    childTravelerAge = 'childTravelerAge=' + flightData['childTravelerAge'] + '&' if 'childTravelerAge' in flightData.keys() else ''
    infantSeatingInLap = 'infantSeatingInLap=' + flightData['infantSeatingInLap'] + '&' if 'infantSeatingInLap' in flightData.keys() else ''
    correlationId = 'correlationId=' + flightData['correlationId'] + '&' if 'correlationId' in flightData.keys() else ''
    maxOfferCount = 'maxOfferCount=' + flightData['maxOfferCount'] + '&' if 'maxOfferCount' in flightData.keys() else ''
    s = Template('http://terminal2.expedia.com/x/mflights/search?$departureAirport$arrivalAirport$departureDate$returnDate$numberOfAdultParameters$childTravelerAge$infantSeatingInLap$correlationId$maxOfferCount')
    search = s.substitute(departureAirport=departureAirport, 
        arrivalAirport=arrivalAirport,
        departureDate=departureDate,
        returnDate=returnDate,
        numberOfAdultParameters=numberOfAdultParameters,
        childTravelerAge=childTravelerAge,
        infantSeatingInLap=infantSeatingInLap,
        correlationId=correlationId,
        maxOfferCount=maxOfferCount) + 'prettyPrint=true&apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'
    response = requests.get(search)
    content = json.loads(response.content)
    return Response(content, status=response.status_code)


@api_view(['POST'])
def flightOverview(request):
    flightData = request.data
    startDate = flightData['startDate'] if 'startDate' in flightData.keys() else '' 
    dayCount = int(flightData['dayCount']) if 'dayCount' in flightData.keys() else 10
    origin = flightData['origin'] if 'origin' in flightData.keys() else '' 
    destination = flightData['destination'] if 'destination' in flightData.keys() else '' 
    
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
    
    if startDate != "" and dayCount > 0: # checking dayCount to avoid user setting dayCount to 0 or negative number on purpose
        post_data["FareCalendar"] = {
            "StartDate" : startDate,
            "DayCount" : dayCount 
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
def carSearch(request):
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
    
    
    flightData = request.data
    pickupdate = 'pickupdate=' + flightData['pickupdate'] + '&' if 'pickupdate' in flightData.keys() else ''
    dropoffdate = 'dropoffdate=' + flightData['dropoffdate'] + '&' if 'dropoffdate' in flightData.keys() else ''
    pickuplocation = 'pickuplocation=' + flightData['pickuplocation'] + '&' if 'pickuplocation' in flightData.keys() else ''
    dropofflocation = 'dropofflocation=' + flightData['dropofflocation'] + '&' if 'dropofflocation' in flightData.keys() else ''
    sort = 'sort=' + flightData['sort'] + '&' if 'sort' in flightData.keys() else ''
    limit = 'limit=' + flightData['limit'] + '&' if 'limit' in flightData.keys() and flightData['limit'] > 0 else 10
    suppliers = 'suppliers=' + flightData['suppliers'] + '&' if 'suppliers' in flightData.keys() else ''
    classes = 'classes=' + flightData['classes'] + '&' if 'classes' in flightData.keys() else ''
    
    s = Template("http://terminal2.expedia.com:80/x/cars/search?$pickupdate$dropoffdate$pickuplocation$dropofflocation$sort$limit$suppliers$classes")
    
    search = s.substitute(pickupdate=pickupdate, 
        dropoffdate=dropoffdate,
        pickuplocation=pickuplocation,
        dropofflocation=dropofflocation,
        sort=sort,
        limit=limit,
        suppliers=suppliers,
        classes=classes) + 'apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'

    response = requests.get(search)
    content = json.loads(response.content)
    return Response(content, status=response.status_code)

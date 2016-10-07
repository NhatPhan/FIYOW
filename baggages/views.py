from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests, json
from string import Template

@api_view(['GET'])
def baggageForPassenger(request):
    """
    pnr (mandatory)
    dep_flight_date (mandatory)
    """    
    passengerData = request.data
    pnr = passengerData['pnr']
    dep_flight_date = passengerData['dep_flight_date']
    
    s = Template('https://bagjourney.sita.aero/baggage/bagsforpassenger/v1.0\
        /pnr/$pnr/dep_flight_date/$dep_flight_date')
    
    custom_headers = { 'Accept-Charset': 'UTF-8',
        'CONTENT-TYPE' : 'application/json',
        'Accept' : 'application/json',
        'api_key' : '2ad03198b7287e91a44d213e696bbb4b'
    }
        
    query = s.substitute(pnr=pnr,dep_flight_date=dep_flight_date) + 'prettyPrint=true&apikey=7989ca6cbadb38855a6112a2eab0d594'
    response = requests.get(query, headers=custom_headers)
    content = json.loads(response.content)
    return Response(content, status=response.status_code)
    
    
    
    
    
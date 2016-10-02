import json
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
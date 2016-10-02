# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests, json
from string import Template

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

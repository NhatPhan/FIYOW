import json
from string import Template

import requests
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import render

@api_view(['POST', 'GET'])
@renderer_classes([TemplateHTMLRenderer])
def activities_search(request):
    """
    location (required)
    startDate
    endDate
    """
    
    if request.method == 'POST':
        activities_data = request.data
        location = 'location=' + activities_data['location'] + '&' if 'location' in activities_data.keys() else ''
        start_date = 'startDate=' + activities_data['startDate'] + '&' if 'startDate' in activities_data.keys() else ''
        end_date = 'endDate=' + activities_data['endDate'] + '&' if 'endDate' in activities_data.keys() else ''
    
        s = Template('http://terminal2.expedia.com:80/x/activities/search?$location$startDate$endDate')
        search = s.substitute(location=location,
                startDate=start_date,
                endDate=end_date) + 'apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'
        response = requests.get(search)
        content = json.loads(response.content)
        return Response(content, status=response.status_code, template_name='bookings/flight-search-result.html')
    
    else:
        return render(request, 'bookings/activities-search.html')


@api_view(["POST"])
def activity_details(request):
    """
    activityId (required)
    startDate
    endDate
    """

    activities_data = request.data
    activity_id = 'activityId=' + activities_data['activityId'] + '&' if 'activityId' in activities_data.keys() else ''
    start_date = 'startDate=' + activities_data['startDate'] + '&' if 'startDate' in activities_data.keys() else ''
    end_date = 'endDate=' + activities_data['endDate'] + '&' if 'endDate' in activities_data.keys() else ''

    s = Template('http://terminal2.expedia.com:80/x/activities/details?$activityId$startDate$endDate')
    search = s.substitute(activityId=activity_id,
            startDate=start_date,
            endDate=end_date) + 'apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'
    response = requests.get(search)
    content = json.loads(response.content)
    return Response(content, status=response.status_code)
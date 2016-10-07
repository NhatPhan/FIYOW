import json
import demjson
from string import Template

import requests

from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

@api_view(['POST', 'GET'])
#@renderer_classes([TemplateHTMLRenderer])
def book_flight(request):
    # Handling flight search
    if request.method == 'POST':
        data = request.data['json_segment']
        data = data.replace("u\'", "\'").replace("\'", "\"").replace("True", "\"True\"").replace("False", "\"False\"")

        json_data = json.loads(data)
        return Response(json_data)


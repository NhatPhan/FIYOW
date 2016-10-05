from django.shortcuts import render

# Create your views here.
from directions.models import Location


def poi_list(request):
    pois = Location.objects.all()

    return render(request, 'directions/map-template-example.html', {'pois': pois})



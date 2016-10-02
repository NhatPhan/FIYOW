import json
from string import Template

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def hotel_search(request):
    """
    city (required)
    regionId
    latitude
    longitude
    filterUnavailable (boolean)
    filterHotelName
    filterStarRatings (0 to 50, increment by 5)
    filterAmenities (list of amenity ids separated by commas)
    sortOrder (boolean)
    resultsPerPage (-1 is reserved for returning ALL matching hotels, default is 25)
    sourceType (mobileapp or mobileweb)
    checkInDate (required, ISO format)
    checkOutDate (required, ISO format)
    room1 (Optional if room field is specified, first number is NoOfAdults, followed by the children's ages, E.g: 2,12,3,2,0 = 2 adults + 4 children with respective age)
    room (Optional if room1 field is specified, same as above)
    """

    hotel_data = request.data
    city = 'city=' + hotel_data['city'] + '&' if 'city' in hotel_data.keys() else ''
    region_id = 'regionId=' + hotel_data['regionId'] + '&' if 'regionId' in hotel_data.keys() else ''
    latitude = 'latitude=' + hotel_data['latitude'] + '&' if 'latitude' in hotel_data.keys() else ''
    longitude = 'longitude=' + hotel_data['longitude'] + '&' if 'longitude' in hotel_data.keys() else ''
    filter_unavailable = 'filterUnavailable=' + hotel_data['filterUnavailable'] + '&' if 'filterUnavailable' in hotel_data.keys() else ''
    filter_hotel_name = 'filterHotelName=' + hotel_data['filterHotelName'] + '&' if 'filterHotelName' in hotel_data.keys() else ''
    filter_star_ratings = 'filterStarRatings=' + hotel_data['filterStarRatings'] + '&' if 'filterStarRatings' in hotel_data.keys() else ''
    filter_amenities = 'filterAmenities=' + hotel_data['filterAmenities'] + '&' if 'filterAmenities' in hotel_data.keys() else ''
    sort_order = 'sortOrder=' + hotel_data['sortOrder'] + '&' if 'sortOrder' in hotel_data.keys() else ''
    results_per_page = 'resultsPerPage=' + hotel_data['resultsPerPage'] + '&' if 'resultsPerPage' in hotel_data.keys() else ''
    source_type = 'sourceType=' + hotel_data['sourceType'] + '&' if 'sourceType' in hotel_data.keys() else ''
    check_in_date = 'checkInDate=' + hotel_data['checkInDate'] + '&' if 'checkInDate' in hotel_data.keys() else ''
    check_out_date = 'checkOutDate=' + hotel_data['checkOutDate'] + '&' if 'checkOutDate' in hotel_data.keys() else ''
    room1 = 'room1=' + hotel_data['room1'] + '&' if 'room1' in hotel_data.keys() else ''
    room = 'room=' + hotel_data['room'] + '&' if 'room' in hotel_data.keys() else ''

    s = Template('http://terminal2.expedia.com:80/x/mhotels/search?$city$regionId$latitude$longitude$filterUnavailable$filterHotelName$filterStarRatings$filterAmenities$filterAmenities$sortOrder$resultsPerPage$sourceType$checkInDate$checkOutDate$room1$room')
    search = s.substitute(city=city,
            regionId=region_id,
            latitude=latitude,
            longitude=longitude,
            filterUnavailable=filter_unavailable,
            filterHotelName=filter_hotel_name,
            filterStarRatings=filter_star_ratings,
            filterAmenities=filter_amenities,
            sortOrder=sort_order,
            resultsPerPage=results_per_page,
            sourceType=source_type,
            checkInDate=check_in_date,
            checkOutDate=check_out_date,
            room1=room1,
            room=room) + 'apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'
    response = requests.get(search)
    content = json.loads(response.content)
    return Response(content, status=response.status_code)
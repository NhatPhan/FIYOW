
import json
from string import Template

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def unreal_deals(request):
    """
    originTLA (required)
    destinationTLA (required)
    startDate (required)
    endDate (required)
    lengthOfStay (required)
    excludedHotels
    roomCount
    adultCount
    childCount
    infantCount
    limit
    stickers
    sortOrder (Asc or Desc)
    sortStrategy (SavingsPercentage)
    minPackagePrice
    maxPackagePrice
    minSavingsPercentage
    maxSavingsPercentage
    allowDuplicates (multiple deals per hotel? boolean)
    """

    deals = request.data
    origin_tla = 'originTLA=' + deals['originTLA'] + '&' if 'originTLA' in deals.keys() else ''
    destination_tla = 'destinationTLA=' + deals['destinationTLA'] + '&' if 'destinationTLA' in deals.keys() else ''
    start_date = 'startDate=' + deals['startDate'] + '&' if 'startDate' in deals.keys() else ''
    end_date = 'endDate=' + deals['endDate'] + '&' if 'endDate' in deals.keys() else ''
    length_of_stay = 'lengthOfStay=' + deals['lengthOfStay'] + '&' if 'lengthOfStay' in deals.keys() else ''
    excluded_hotels = 'excludedHotels=' + deals['excludedHotels'] + '&' if 'excludedHotels' in deals.keys() else ''
    room_count = 'roomCount=' + deals['roomCount'] + '&' if 'roomCount' in deals.keys() else ''
    adult_count = 'adultCount=' + deals['adultCount'] + '&' if 'adultCount' in deals.keys() else ''
    child_count = 'childCount=' + deals['childCount'] + '&' if 'childCount' in deals.keys() else ''
    infant_count = 'infantCount=' + deals['infantCount'] + '&' if 'infantCount' in deals.keys() else ''
    limit = 'limit=' + deals['limit'] + '&' if 'limit' in deals.keys() else ''
    stickers = 'stickers=' + deals['stickers'] + '&' if 'stickers' in deals.keys() else ''
    sort_order = 'sortOrder=' + deals['sortOrder'] + '&' if 'sortOrder' in deals.keys() else ''
    sort_strategy = 'sortStrategy=' + deals['sortStrategy'] + '&' if 'sortStrategy' in deals.keys() else ''
    min_package_price = 'minPackagePrice=' + deals['minPackagePrice'] + '&' if 'minPackagePrice' in deals.keys() else ''
    max_package_price = 'maxPackagePrice=' + deals['maxPackagePrice'] + '&' if 'maxPackagePrice' in deals.keys() else ''
    min_savings_percentage = 'minSavingsPercentage=' + deals['minSavingsPercentage'] + '&' if 'minSavingsPercentage' in deals.keys() else ''
    max_savings_percentage = 'maxSavingsPercentage=' + deals['maxSavingsPercentage'] + '&' if 'maxSavingsPercentage' in deals.keys() else ''
    allow_duplicates = 'allowDuplicates=' + deals['allowDuplicates'] + '&' if 'allowDuplicates' in deals.keys() else ''

    s = Template('http://terminal2.expedia.com:80/x/deals/packages?$originTLA$destinationTLA$startDate$endDate$lengthOfStay$excludedHotels$roomCount$adultCount$childCount$infantCount$limit$stickers$sortOrder$sortStrategy$minPackagePrice$maxPackagePrice$minSavingsPercentage$maxSavingsPercentage$allowDuplicates')
    search = s.substitute(originTLA=origin_tla,
            destinationTLA=destination_tla,
            startDate=start_date,
            endDate=end_date,
            lengthOfStay=length_of_stay,
            excludedHotels=excluded_hotels,
            roomCount=room_count,
            adultCount=adult_count,
            childCount=child_count,
            infantCount=infant_count,
            limit=limit,
            stickers=stickers,
            sortOrder=sort_order,
            sortStrategy=sort_strategy,
            minPackagePrice=min_package_price,
            maxPackagePrice=max_package_price,
            minSavingsPercentage=min_savings_percentage,
            maxSavingsPercentage=max_savings_percentage,
            allowDuplicates=allow_duplicates) + 'apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'
    response = requests.get(search)
    content = json.loads(response.content)
    return Response(content, status=response.status_code)
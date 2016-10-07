from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from bookings.models import Hotel
from users.models import SIAUser


def hotel_booking(request):
    if request.method == 'POST':
        SIAUserId = SIAUser.objects.get(user__id=request.user.id)
        hotel = Hotel(user=SIAUserId, hotelId=request.POST['hotelId'])
        hotel.save()
        return HttpResponseRedirect(reverse('trip'))
    return HttpResponseRedirect(reverse('hotel-search'))
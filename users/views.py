from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.generic.edit import ModelFormMixin
from django.views.generic import DetailView
from rest_framework import serializers

from baggages.models import Baggage
from users.forms import SIAUserForm, LocationFormSet
from users.models import SIAUser
from bookings.models import Hotel, AttractionTicket, Booking
from directions.models import Location
import json
from string import Template

import requests
from rest_framework.decorators import api_view
from collections import defaultdict
from rest_framework.response import Response

from datetime import datetime

def test(request):
    """
    To test template
    :param request:
    :return:
    """

    return render(request, 'users/template.html')


def index(request):
    """
    Main entry for the website, also handling login request
    :param request:
    :return:
    """

    # Handling login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('flight-search'))

        else:
            # Render with error message
            error = "Wrong username/password"
            return render(request, 'users/index.html', {'error': error})

    else:
        return render(request, 'users/index.html')


def signup(request):
    """
    for user to register for an account
    :param request:
    :return:
    """

    if request.user.is_authenticated():
        user = request.user
        pass
        # TODO redirect to profile page

    if not request.method == 'POST':
        return render(request, 'users/signup.html')

    password = request.POST.get('password')
    username = request.POST.get('username')
    email = request.POST.get('email')

    last_name = request.POST.get('lastname')
    first_name = request.POST.get('firstname')

    # Django user authentication table
    user = User.objects.create_user(username, email, password)
    user.save()

    # SIA User record
    sia_user = SIAUser.create(user=user, first_name=first_name, last_name=last_name)
    sia_user.save()

    # Login
    user_authenticated = authenticate(username=username, password=password)
    login(request, user_authenticated)

    return HttpResponseRedirect(reverse('profile'))


class ProfileView(ModelFormMixin, DetailView):
    """
    Profile dashboard of user
    :param request:
    :return:
    """
    template_name = 'users/profile.html'
    model = SIAUser
    form_class = SIAUserForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        location_form = LocationFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form, location_form=location_form))
    
    def get_success_url(self):
        return reverse('profile')

    def get_context_data(self, form, location_form, **kwargs):
        user_profile = SIAUser.objects.get(user__id=self.request.user.id)
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['form'] = form
        context['location_form'] = location_form
        context['SiaUser'] = user_profile
        return context
        
    def get_object(self,**kwargs):
        user_profile = SIAUser.objects.get(user__id=self.request.user.id)
        return user_profile
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        location_form = LocationFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        if form.is_valid() and location_form.is_valid():
            return self.form_valid(form, location_form)
        else:
            return self.form_invalid(form, location_form)
    
    def form_valid(self, form, location_form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        self.object = form.save()
        location_form.instance = self.object
        location_form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form, location_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, location_form=location_form))

@api_view(['GET'])
def trip(request):
    """
    Trip view of the user
    :param request:
    :return:
    """

    # Authentication check
    if not request.user.is_authenticated():
        # TODO redirect to error page
        return redirect(reverse('index'))

    user = request.user

    sia_user = get_object_or_404(SIAUser, user=user)
    hotels = Hotel.objects.filter(user=sia_user)
    activities = AttractionTicket.objects.filter(user=sia_user)
    bookings = Booking.objects.filter(user=sia_user)

    hotelsResponse = []
    activitiesResponse = []


    for hotel in hotels:
        hotel_id = 'hotelId=' + str(hotel.hotelId)

        s = Template('http://terminal2.expedia.com:80/x/mhotels/info?$hotelId')
        search = s.substitute(hotelId=hotel_id) + '&apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'
        hotel = requests.get(search)
        content = json.loads(hotel.content)
        newHotelResponse = {}
        
        hotelName = content['localizedHotelName']
        if 'checkInInstructions' in content:
            checkInInstructions = content['checkInInstructions']
            newHotelResponse['checkInInstructions'] = checkInInstructions
        hotelAddress = content['hotelAddress']
        telesalesNumber = content['telesalesNumber']
        
        if 'largeThumbnailUrl' in content:
            image = content['largeThumbnailUrl']
            newHotelResponse['image'] = image
        
        newHotelResponse['hotelName'] = hotelName
        newHotelResponse['hotelAddress'] = hotelAddress
        newHotelResponse['telesalesNumber'] = telesalesNumber
        

        
        hotelsResponse.append(newHotelResponse)
    
        
    for activity in activities:
        
        activity_id = 'activityId=' + str(activity.activityId)
        start_date = '&startDate=' + str(activity.start_date)
        end_date = '&endDate=' + str(activity.end_date)
        
        s = Template('http://terminal2.expedia.com:80/x/activities/details?$activityId$startDate$endDate')
        search = s.substitute(activityId=activity_id,
                startDate=start_date,
                endDate=end_date) + '&apikey=xVKsMHTYGMyM5xXp2iyIABHnbx3j8l44'
                
        response = requests.get(search)
        content = json.loads(response.content)
        newActivityResponse = {}
        
        activityTitle = content['title']
        
        newActivityResponse['title'] = activityTitle
        
        activityCategory = content['category']
        
        newActivityResponse['category'] = activityCategory
        
        activityStart = content['startDate']
        
        newActivityResponse['startDate'] = activityStart
        
        activityEnd = content['endDate']
        
        newActivityResponse['endDate'] = activityEnd
        
        activityImage = content['images'][0]['url']
        
        newActivityResponse['image'] = activityImage
        
        activitiesResponse.append(newActivityResponse)

    return render(request, 'users/trip.html',
                  {'SiaUser':sia_user,
                   'bookings': bookings,
                   'hotels': hotelsResponse,
                   'activities': activitiesResponse })


def onflight(request):
    """
    On flight view for the user
    :param request:
    :return:
    """

    # Authentication check
    if not request.user.is_authenticated():
        # TODO redirect to error page
        return redirect(reverse('index'))

    user = request.user

    sia_user = get_object_or_404(SIAUser, user=user)
    return render(request, 'users/on-flight.html', {'SiaUser':sia_user})
    
def onflightfr(request):
    """
    On flight view for the user - in fr
    :param request:
    :return:
    """
    
    # Authentication check
    if not request.user.is_authenticated():
        # TODO redirect to error page
        return redirect(reverse('index'))

    user = request.user

    sia_user = get_object_or_404(SIAUser, user=user)
    return render(request, 'users/on-flight-fr.html', {'SiaUser':sia_user})    

@api_view(['GET'])
def arrival(request):
    """
    On arrival view for the user
    :param request:
    :return:
    """

    # Authentication check
    if not request.user.is_authenticated():
        # TODO redirect to error page
        return redirect(reverse('index'))

    user = request.user

    sia_user = get_object_or_404(SIAUser, user=user)

    # baggage

    result = []
    bookings = Booking.objects.filter(user=sia_user)
    for booking in bookings:
        baggages = Baggage.objects.filter(booking=booking)
        if len(baggages) > 0:
            result.append((booking.id, baggages))

    print(result)


    # taxi
    pois = Location.objects.all()
    return render(request, 'users/arrival.html',
                  {'SiaUser':sia_user, 'pois': pois, 'bookings': result} )
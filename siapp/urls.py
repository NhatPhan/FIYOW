"""siapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from bookings.views import *
from users.views import *
from baggages.views import baggageStatus, addBaggageForBooking
from directions.views import *
from chat.views import chat_view

from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    # Index
    url(r'^$', index, name='index'),

    # Expedia APIs
    url(r'^expedia/flight_search', flight_search, name='flight-search'),
    url(r'^expedia/flight_overview', flight_overview),
    url(r'^expedia/car_search', car_search),
    url(r'^expedia/car_search', car_search),
    url(r'^expedia/hotel_search', hotel_search, name='hotel-search'),
    url(r'^expedia/hotel_offers', hotel_offers),
    url(r'^expedia/hotel_info', hotel_info),
    url(r'^expedia/hotel_booking', hotel_booking, name='hotel-booking'),
    url(r'^expedia/package_search', package_search),
    url(r'^expedia/activities_search', activities_search, name='activities-search'),
    url(r'^expedia/activity_details', activity_details),
    url(r'^expedia/activity_booking', activity_booking, name='activity_booking'),
    url(r'^expedia/unreal_deals', unreal_deals),

    # Users
    url(r'^user/signup$', signup, name='signup'),
    url(r'^user/profile$', login_required(ProfileView.as_view()), name='profile'),
    url(r'^user/trip', trip, name='trip'),
    url(r'^testtemplate$', test, name='test'),

    # Baggage
    url(r'^user/baggages$', baggageStatus),
    url(r'^add_baggages$', addBaggageForBooking),

    # Direction
    url(r'^map$', poi_list , name='poi_list'),

    # Chat
    url(r'^chat/', chat_view, name='chat'),
    
    # On flight
    url(r'^onflight/', onflight, name='onflight'),
    url(r'^onflight/fr/', onflightfr, name='onflightfr'),
    
    # Arrival
    url(r'^arrival/', arrival, name='arrival'),

    url(r'^expedia/book_flight', book_flight, name='book_flight1')
]


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from users.forms import SIAUserForm, LocationFormSet
from users.models import SIAUser

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


def profile(request):
    """
    Profile dashboard of user
    :param request:
    :return:
    """

    # Authentication check
    if not request.user.is_authenticated():
        # TODO redirect to error page
        return redirect(reverse('index'))

    user = request.user
    sia_user = SIAUser.objects.get(user=user)

    userForm = SIAUserForm(request.POST,request.FILES,instance=sia_user)
    locationForm = LocationFormSet(request.POST,request.FILES,instance=sia_user)

    sia_user = get_object_or_404(SIAUser, user=user)
    return render(request, 'users/profile.html', {'siaUser':sia_user, 'userForm':userForm, 'locationForm':locationForm })


def trip(request):
    """
    Profile dashboard of user
    :param request:
    :return:
    """

    # Authentication check
    if not request.user.is_authenticated():
        # TODO redirect to error page
        return redirect(reverse('index'))

    user = request.user

    sia_user = get_object_or_404(SIAUser, user=user)
    return render(request, 'users/trip.html', {'siaUser':sia_user})

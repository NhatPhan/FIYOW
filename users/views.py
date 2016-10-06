from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.generic.edit import ModelFormMixin
from django.views.generic import DetailView

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


class ProfileView(ModelFormMixin, DetailView):
    """
    Profile dashboard of user
    :param request:
    :return:
    """
<<<<<<< HEAD
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
    
=======

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
>>>>>>> d5e387252ed1e47349eac0a90b8d54ed3d80523d

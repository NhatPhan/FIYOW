from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from users.models import SIAUser
from directions.models import Location

from django.forms.widgets import SelectDateWidget


class SIAUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=200, required=False)
    last_name = forms.CharField(max_length=200, required=False)
    postal_address = forms.CharField(max_length=500, required=False)
    residence_country = forms.CharField(max_length=200, required=False)
    nationality = forms.CharField(max_length=200, required=False)
    dob = forms.DateField(widget=SelectDateWidget(years=range(1900, 2020), empty_label=("Choose Year", "Choose Month", "Choose Day")), required=False)
    language = forms.CharField(max_length=200, required=False)
    
    #Credit Card Info
    name_on_card = forms.CharField(max_length=200, required=False)
    card_number = forms.CharField(max_length=20, required=False)
    expiration_month = forms.IntegerField(required=False)
    expiration_year = forms.IntegerField(required=False)
    cvv_number = forms.IntegerField(required=False)

    class Meta:
        model = SIAUser
        fields = ('first_name','last_name', 'postal_address', 'residence_country', 'nationality', 'dob', 'language',
        'name_on_card', 'card_number', 'expiration_month', 'expiration_year', 'cvv_number')


LocationFormSet = inlineformset_factory(SIAUser, Location, fields=('user', 'location_name', 'position'), 
    max_num=1, extra=1, can_delete=False
)
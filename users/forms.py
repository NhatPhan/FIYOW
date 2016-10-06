from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from users.models import SIAUser
from directions.models import Location

from django.forms.widgets import SelectDateWidget


class SIAUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=200)

    class Meta:
        model = SIAUser
        fields = ('first_name',)


LocationFormSet = inlineformset_factory(SIAUser, Location,
                                        fields=('user', 'name', 'position'), max_num=1,
                                        extra=1, can_delete=False)
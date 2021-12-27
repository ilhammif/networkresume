from django import forms
from django.forms import widgets
from django.forms.widgets import HiddenInput
from .models import Site_Profile

class Site_Profile_form(forms.ModelForm):
    class Meta:
        model = Site_Profile
        fields =['site_id_profile','Week', 'Year','Year_Week',]#
        labels = {'site_id_profile':'Excel Site Profile'}
        widgets = {'Year_Week': forms.HiddenInput()}
        
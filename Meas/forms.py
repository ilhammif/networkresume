from django import forms
from .models import Meas

class Meas_form(forms.ModelForm):
    class Meta:
        model = Meas
        fields =['Meas2G','Meas3G','Meas4G','Week', 'Year','Year_Week',]#
        labels = {'Meas2G':'Excel Meas 2G',
                    'Meas3G':'Excel Meas 3G',
                    'Meas4G':'Excel Meas 4G'
                }
        widgets = {'Year_Week': forms.HiddenInput()}
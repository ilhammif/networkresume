from django import forms
from .models import RNC

class RNC_form(forms.ModelForm):
    class Meta:
        model = RNC
        fields =['Name','RNC']#
        labels = {'Nodin':'Excel RNC'}
        widgets = {'Name': forms.HiddenInput(),
                    }
        
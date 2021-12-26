from django import forms
from .models import Nodin_To_Tpass

class Nodin_To_Tpass_form(forms.ModelForm):
    class Meta:
        model = Nodin_To_Tpass
        fields =['Name','RNC_fields','Nodin_fields','tpass_fields']#
        labels = {'Nodin_fields':'Select Nodin',
                    'RNC_fields':'Select RNC'
        }
        widgets = {'Name': forms.HiddenInput(),
                    'tpass_fields':forms.HiddenInput(),
                    }
        
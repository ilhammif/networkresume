from django import forms
from .models import Nodin

class Nodin_form(forms.ModelForm):
    class Meta:
        model = Nodin
        fields =['Name','Nodin']#
        labels = {'Nodin':'Excel Nodin'}
        widgets = {'Name': forms.HiddenInput(),
                    }
        
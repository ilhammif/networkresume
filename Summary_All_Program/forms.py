from django import forms
from django.forms import widgets
from django.forms.widgets import HiddenInput
from .models import Summary_All_Program, Summary_All_Program_Checker,SAP_Filter

class Summary_All_Program_form(forms.ModelForm):
    class Meta:
        model = Summary_All_Program
        fields =['summary_all_program','Week', 'Year','Year_Week',]#
        labels = {'summary_all_program':'Excel Summary All Program'}
        widgets = {'Year_Week': forms.HiddenInput()}

class SAP_Filter_form(forms.ModelForm):
    class Meta:
        model = SAP_Filter
        fields =['SAP_Filter','Week', 'Year','Year_Week',]#
        labels = {'SAP_Filter':'Summary All Program Filter'}
        widgets = {'Year_Week': forms.HiddenInput()}

class Summary_All_Program_Checker_form(forms.ModelForm):
    class Meta:
        model = Summary_All_Program_Checker
        fields = {'summary_all_program','SAP_Filter','Week', 'Year','Year_Week'}
        labels = {'summary_all_program':'Summary All Program',
                    'SAP_Filter':'Previous Summary All Program Filter',
                    }
        widgets = {'Year_Week': forms.HiddenInput()}
    field_order = ['summary_all_program','SAP_Filter','Week', 'Year',]
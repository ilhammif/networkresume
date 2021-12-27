from django import forms
from .models import NOC_Processing

class NOC_Processing_form(forms.ModelForm):
    class Meta:
        model = NOC_Processing
        fields =['Name','Year_Week','lw_fields','cw_fields','site_profile_fields','NOC_fields','Week','Year']#
        labels = {'lw_fields':'Select W-1 Measurements',
                    'cw_fields':'Select W-0 Measurements',
                    'site_profile_fields':'Select Site Profile'
        }
        widgets = {'Year_Week':forms.HiddenInput(),
                'Name':forms.HiddenInput(),
                'NOC_fields':forms.HiddenInput(),
                    }
        
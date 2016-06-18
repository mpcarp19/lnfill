from django import forms
from django.forms import ModelForm
from lnmain.models import LNFillConf
 
class ConfigForm(forms.Form):
    chan    = forms.CharField()
    ctype   = forms.CharField()
    cname   = forms.CharField()
    cenable = forms.CharField()

class LNFillConfForm(ModelForm):
    class Meta:
        model = LNFillConf
        fields = ['ch_type', 'ch_name', 'ch_enable']






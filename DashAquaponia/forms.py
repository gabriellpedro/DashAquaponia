from django import forms
from .models import DashModel

class DashForm(forms.ModelForm):
    class Meta:
        model = DashModel
        fields = '__all__'
        widgets = {
            'valorAlface': forms.NumberInput(attrs={'step': '0.01'}),
            'valorPeixe': forms.NumberInput(attrs={'step': '0.01'})
        }
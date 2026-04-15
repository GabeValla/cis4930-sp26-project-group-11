from django import forms
from .models import CrimeIncident

class CrimeIncidentForm(forms.ModelForm):
    class Meta:
        model = CrimeIncident
        fields = ['city', 'date_time', 'reason', 'location', 'latitude', 'longitude']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.TextInput(attrs={'placeholder': 'e.g. THEFT, BURGLARY'}),
        }

from django import forms
from apps.app.models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['description_service']

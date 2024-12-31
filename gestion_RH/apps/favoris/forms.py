from django import forms
from apps.app.models import Fonctionnalite

class FonctionnaliteForm(forms.ModelForm):
    class Meta:
        model = Fonctionnalite
        fields = '__all__'  

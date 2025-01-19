

from django import forms
from apps.app.models import Offre_employe

class OffreEmployeForm(forms.ModelForm):
    date_posted = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Offre_employe
        fields = '__all__'  

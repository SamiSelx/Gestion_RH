

from django import forms
from apps.app.models import Offre_employe

class OffreEmployeForm(forms.ModelForm):
    class Meta:
        model = Offre_employe
        fields = '__all__'  

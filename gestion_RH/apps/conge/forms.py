from django import forms
from .models import Conge

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = ['code', 'employe', 'date_debut', 'date_fin', 'type_conge', 'description']

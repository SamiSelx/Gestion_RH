from django import forms
from apps.app.models import Employe

class EmployeForm(forms.ModelForm):
    date_naissance_E = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_embauche_E = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Employe
        fields = '__all__'  

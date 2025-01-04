from django import forms
from ..app.models import Contrat

class ContratForm(forms.ModelForm):
    date_debut_contrat = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_fin_contrat = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Contrat
        fields = "__all__"

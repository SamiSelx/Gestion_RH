from django import forms
from ..app.models import Objectif

class ObjectifForm(forms.ModelForm):
    date_limite = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Objectif
        fields = "__all__"

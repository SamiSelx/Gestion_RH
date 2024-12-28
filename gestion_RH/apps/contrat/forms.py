from django import forms
from ..app.models import Contrat

class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = "__all__"

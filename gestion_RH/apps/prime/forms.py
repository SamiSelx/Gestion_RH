from django import forms
from ..app.models import Prime

class PrimeForm(forms.ModelForm):
    class Meta:
        model = Prime
        fields = ['code_employe','prime_montant']
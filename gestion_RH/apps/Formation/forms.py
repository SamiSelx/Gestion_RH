from django import forms
from apps.app.models import Formation


class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['titre_formation', 'description_formation']

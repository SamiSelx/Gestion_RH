from django import forms
from apps.app.models import Candidature , Entretien

class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['candidat','cv']

class EntretienForm(forms.ModelForm):
    class Meta:
        model = Entretien
        fields = ['date_entretien', 'lieu', 'commentaires']

class CandidatureStatusForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['statut']
        
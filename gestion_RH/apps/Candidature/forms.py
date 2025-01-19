from django import forms
from apps.app.models import Candidature , Entretien,Candidat

class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['cv']

    def __init__(self, *args, **kwargs):
        self.candidat_id = kwargs.pop('candidat_id', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.candidat_id:
            instance.candidat = Candidat.objects.get(id=self.candidat_id)
        if commit:
            instance.save()
        return instance
    
class EntretienForm(forms.ModelForm):
    class Meta:
        model = Entretien
        fields = ['date_entretien', 'lieu', 'commentaires']

class CandidatureStatusForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['statut']
        
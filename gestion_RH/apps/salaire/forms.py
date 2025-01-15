from django import forms
from ..app.models import Absence,Employe,DemandeAvanceSalaire,Prime

class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['date_absence']

# Employe demande conge
class DemandeAvanceSalaireForm(forms.ModelForm):
    class Meta:
        model = DemandeAvanceSalaire
        fields = ['montant', 'justifications'] 

    def __init__(self, *args, **kwargs):
        self.employe_id = kwargs.pop('employe_id', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.employe_id:
            instance.code_employe = Employe.objects.get(id=self.employe_id)
        if commit:
            instance.save()
        return instance
    
class PrimeForm(forms.ModelForm):
    class Meta:
        model = Prime
        fields = ['code_employe','prime_montant']
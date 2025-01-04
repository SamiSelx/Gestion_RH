from django import forms
from ..app.models import Conge,DemandeConge,Employe

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = "__all__"

# Employe demande conge
class DemandeCongeForm(forms.ModelForm):
    date_debut = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = DemandeConge
        fields = ['code_conge','date_debut', 'date_fin'] 

    def __init__(self, *args, **kwargs):
        self.employe_id = kwargs.pop('employe_id', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.employe_id:
            instance.code_employe = Employe.objects.get(id=self.employe_id)
        if commit:
            instance.calculer_jours_demandes()
            instance.save()
        return instance
    

class CongeFilterForm(forms.Form):
    employe = forms.ModelChoiceField(queryset=Employe.objects.all(), required=False)
    # type_conge = forms.ChoiceField(choices=Conge.type_conge, required=False)
    type_conge = forms.ModelChoiceField(queryset=Conge.objects.all(), required=False)
    date_debut_from = forms.DateField(required=False, widget=forms.SelectDateWidget)
    date_debut_to = forms.DateField(required=False, widget=forms.SelectDateWidget)

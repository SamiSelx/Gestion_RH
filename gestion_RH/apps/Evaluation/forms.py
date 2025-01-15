from django import forms
from apps.app.models import Evaluation, EvaluerCritere , CriterEvaluation,Objectif

class EvaluationForm(forms.ModelForm):
    date_evaluation = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Evaluation
        fields = ['date_evaluation', 'type_evaluation', 'employe_manager', 'employe']

class EvaluerCritereForm(forms.ModelForm):
    class Meta:
        model = EvaluerCritere
        fields = ['code_critere', 'note_critere_evaluer']

class CriterEvaluationForm(forms.ModelForm):
    class Meta:
        model = CriterEvaluation
        fields = ['description_critere']

class ObjectifForm(forms.ModelForm):
    date_limite = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Objectif
        fields = ['description_objectif', 'date_limite']
        widgets = {
            'description_objectif': forms.Textarea(attrs={'class': 'form-control'}),
            'date_limite': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
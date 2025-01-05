from django import forms
from apps.app.models import Evaluation, EvaluerCritere , CriterEvaluation

class EvaluationForm(forms.ModelForm):
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
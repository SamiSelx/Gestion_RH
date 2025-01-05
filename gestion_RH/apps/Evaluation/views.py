from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from apps.app.models import Evaluation,RapportEvaluation, CriterEvaluation , EvaluerCritere
from .forms import EvaluationForm, EvaluerCritereForm , CriterEvaluationForm
from datetime import date


def list_evaluations(request):
    evaluations = Evaluation.objects.all()
    for evaluation in evaluations:
       evaluation.criteria_scores = EvaluerCritere.objects.filter(code_evaluation=evaluation)
    return render(request, 'pages/Manager/Evaluation/list_evaluations.html', {'evaluations': evaluations})


def create_evaluation(request):
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save()
            return redirect('add_criteria_scores', pk=evaluation.pk)
    else:
        form = EvaluationForm()
    return render(request, 'pages/Manager/Evaluation/create_evaluation.html', {'form': form})


def update_evaluation(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return redirect('list_evaluations')
    else:
        form = EvaluationForm(instance=evaluation)
    return render(request, 'pages/Manager/Evaluation/update_evaluation.html', {'form': form})


def delete_evaluation(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        evaluation.delete()
        return redirect('list_evaluations')
    return render(request, 'pages/Manager/Evaluation/delete_evaluation.html', {'evaluation': evaluation})

#----------------------------------------------------------------------
def add_criteria_scores(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        form = EvaluerCritereForm(request.POST)
        if form.is_valid():
            eval_critere = form.save(commit=False)
            eval_critere.code_evaluation = evaluation
            eval_critere.save()
            return redirect('add_criteria_scores', pk=pk)  
    else:
        form = EvaluerCritereForm()
    return render(request, 'pages/Manager/Evaluation/add_criteria_scores.html', {'form': form, 'evaluation': evaluation})


#------------------------------------------------------------
def generate_report(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    contenu = f"Rapport d'évaluation pour {evaluation.employe.nomE}:\n"
    contenu += f"Date d'évaluation: {evaluation.date_evaluation}\n"
    contenu += f"Type: {evaluation.type_evaluation}\n"
    contenu += f"Note totale: {evaluation.note_evaluation_totale}\n"

   
    report, created = RapportEvaluation.objects.get_or_create(
        code_evaluation=evaluation,
        defaults={'contenu_rapport': contenu, 'date_rapport': date.today()},
    )

   
    context = {
        'evaluation': evaluation,
        'report': report,
        'contenu_rapport': report.contenu_rapport.split("\n"), 
    }
    return render(request, 'pages/Manager/Evaluation/evaluation_report.html', context)
#-------------------------------------------------
def top_employees(request):
    period = request.GET.get('period', 'Annual')
    evaluations = Evaluation.objects.filter(type_evaluation=period)
    top_employees = evaluations.values('employe').annotate(avg_score=Avg('note_evaluation_totale')).order_by('-avg_score')[:5]
    return render(request, 'pages/Manager/Evaluation/top_employees.html', {'top_employees': top_employees, 'period': period})
    




#-----------------criteres----------------------------------

def list_criteres(request):
    criteres = CriterEvaluation.objects.all()
    return render(request, 'pages/Manager/Critere/list_criteres.html', {'criteres': criteres})

def create_critere(request):
    if request.method == 'POST':
        form = CriterEvaluationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_criteres')
    else:
        form = CriterEvaluationForm()
    return render(request, 'pages/Manager/Critere/create_critere.html', {'form': form})

def update_critere(request, pk):
    critere = get_object_or_404(CriterEvaluation, pk=pk)
    if request.method == 'POST':
        form = CriterEvaluationForm(request.POST, instance=critere)
        if form.is_valid():
            form.save()
            return redirect('list_criteres')
    else:
        form = CriterEvaluationForm(instance=critere)
    return render(request, 'pages/Manager/Critere/update_critere.html', {'form': form})

def delete_critere(request, pk):
    critere = get_object_or_404(CriterEvaluation, pk=pk)
    if request.method == 'POST':
        critere.delete()
        return redirect('list_criteres')
    return render(request, 'pages/Manager/Critere/delete_critere.html', {'critere': critere})

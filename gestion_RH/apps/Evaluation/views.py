from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from apps.app.models import Evaluation,RapportEvaluation, CriterEvaluation , EvaluerCritere , Objectif, ObjectifAttient ,Employe
from .forms import EvaluationForm, EvaluerCritereForm , CriterEvaluationForm ,ObjectifForm
from datetime import date
from django.contrib import messages

#------------Evaluation-------------------------------------
def list_evaluations(request):
    evaluations = Evaluation.objects.all()
    return render(request, 'pages/Manager/Evaluation/list_evaluations.html', {'evaluations': evaluations})

def list_evaluations_consultation(request):
    evaluations = Evaluation.objects.all()
    return render(request, 'pages/RH/consultation/list_evaluations_consultation.html', {'evaluations': evaluations})


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
            messages.success(request, "Critère ajouté avec succès.")
            return redirect('add_criteria_scores', pk=pk) 
        else:
            messages.error(request, "Erreur lors de l'ajout du critère.")
    else:
        form = EvaluerCritereForm()
    
    context = {
        'form': form,
        'evaluation': evaluation,
    }
    return render(request, 'pages/Manager/Evaluation/add_criteria_scores.html', context)

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

   
    objectifs = ObjectifAttient.objects.filter(code_evaluation=evaluation)
    context = {
    'evaluation': evaluation,
    'report': report,
    'contenu_rapport': report.contenu_rapport.split("\n"),
    'objectifs': objectifs,
     }
    return render(request, 'pages/Manager/Evaluation/evaluation_report.html', context)

#--------------------------------------------------------------





#-------------------------------------------------
def top_employees(request):
    period = request.GET.get('period', 'Annual')
    evaluations = Evaluation.objects.filter(type_evaluation=period)
    top_employees = evaluations.values('employe').annotate(avg_score=Avg('note_evaluation_totale')).order_by('-avg_score')[:5]
    return render(request, 'pages/Manager/Evaluation/top_employees.html', {'top_employees': top_employees, 'period': period})
    

def modal_criteria_view(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    evaluated_criteria = EvaluerCritere.objects.filter(code_evaluation=evaluation)

    context = {
        'evaluation': evaluation,
        'evaluated_criteria': evaluated_criteria,
    }
    return render(request, 'pages/Manager/Evaluation/modal_criteria.html', context)
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




def faire_evaluation(request, evaluation_id):

    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    criteria = evaluation.evaluercritere_set.all()

    if request.method == 'POST':
        total_score = 0
        
        for critere in criteria:
           
            note = int(request.POST.get(f"score_{critere.id}", 0))

            if note > critere.note_critere_evaluer:
                messages.error(request, f"La note pour {critere.code_critere.description_critere} ne peut pas dépasser {critere.note_critere_evaluer}.")
                return render(request, 'pages/Manager/Evaluation/faire_evaluation.html', {'evaluation': evaluation, 'criteria': criteria})

            total_score += note

        evaluation.note_evaluation_totale = total_score
        evaluation.save()

        messages.success(request, "Évaluation faite avec succès.")
        return redirect('list_evaluations') 
    
    return render(request, 'pages/Manager/Evaluation/faire_evaluation.html', {'evaluation': evaluation, 'criteria': criteria})


#----Objective--------------------------------------
def objectifs_pour_evaluation(request, employe_id, evaluation_id):
    employe = get_object_or_404(Employe, id=employe_id)
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)

    objectifs = Objectif.objects.filter(code_employe=employe)
    objectifs_attients = ObjectifAttient.objects.filter(code_evaluation=evaluation)

    if request.method == "POST":
        form = ObjectifForm(request.POST)
        if form.is_valid():
            objectif = form.save(commit=False)
            objectif.code_employe = employe
            objectif.save()
            return redirect('objectifs_pour_evaluation', employe_id=employe.id, evaluation_id=evaluation.id)
    else:
        form = ObjectifForm()

    context = {
        'employe': employe,
        'evaluation': evaluation,
        'objectifs': objectifs,
        'objectifs_attients': objectifs_attients,
        'form': form,
    }
    return render(request, 'pages/Manager/objectif/objectifs_pour_evaluation.html', context)

def marquer_objectif_attient(request, evaluation_id, objectif_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    objectif = get_object_or_404(Objectif, id=objectif_id)
    objectif_attient, created = ObjectifAttient.objects.get_or_create(
        code_evaluation=evaluation, code_objectif=objectif
    )
    objectif_attient.attient = not objectif_attient.attient
    objectif_attient.save()
    return redirect('objectifs_pour_evaluation', employe_id=objectif.code_employe.id, evaluation_id=evaluation.id)




from django.shortcuts import render,redirect
from ..app.models import Competence
from .forms import CompetenceForm

# Create your views here.

def listeCompetence(request):
    competences = Competence.objects.all()
    return render(request,"pages/RH/tables/competence/listeCompetence.html",{'competences':competences})

def ajouterCompetence(request):
    if request.method == 'POST':
        form = CompetenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeCompetence')
    else:
        form = CompetenceForm()
    return render(request,"pages/RH/tables/competence/ajouterCompetence.html",{'form':form})

def modifierCompetence(request,pk):
    competence = Competence.objects.get(id=pk)
    if request.method == 'POST':
        form = CompetenceForm(request.POST,instance=competence)
        if form.is_valid():
            form.save()
            return redirect('listeCompetence')
    else:
        form = CompetenceForm(instance=competence)
    return render(request,'pages/RH/tables/competence/modifierCompetence.html',{'form':form})

def supprimerCompetence(request,pk):
    competence = Competence.objects.get(id=pk)
    if request.method == 'POST':
        competence.delete()
        return redirect('listeCompetence')
    else:
        form = CompetenceForm(instance=competence)
    return render(request,'pages/RH/tables/competence/supprimercompetence.html',{'form':form})
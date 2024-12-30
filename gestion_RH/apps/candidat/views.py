from django.shortcuts import render,redirect
from ..app.models import Candidat
from .forms import CandidatForm

# Create your views here.

def listeCandidat(request):
    candidats = Candidat.objects.all()
    return render(request,"pages/RH/tables/candidat/listeCandidat.html",{'candidats':candidats})

def ajouterCandidat(request):
    if request.method == 'POST':
        form = CandidatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeCandidat')
    else:
        form = CandidatForm()
    return render(request,"pages/RH/tables/candidat/ajouterCandidat.html",{'form':form})

def modifierCandidat(request,pk):
    candidat = Candidat.objects.get(id=pk)
    if request.method == 'POST':
        form = CandidatForm(request.POST,instance=candidat)
        if form.is_valid():
            form.save()
            return redirect('listeCandidat')
    else:
        form = CandidatForm(instance=candidat)
    return render(request,'pages/RH/tables/candidat/modifierCandidat.html',{'form':form})

def supprimerCandidat(request,pk):
    candidat = Candidat.objects.get(id=pk)
    if request.method == 'POST':
        candidat.delete()
        return redirect('listeCandidat')
    else:
        form = CandidatForm(instance=Candidat)
    return render(request,'pages/RH/tables/candidat/supprimerCandidat.html',{'form':form})
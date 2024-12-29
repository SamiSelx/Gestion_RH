from django.shortcuts import render,redirect
from ..app.models import Contrat
from .forms import ContratForm

# Create your views here.

def afficheContrat(request):
    contrats = Contrat.objects.all()
    return render(request,"pages/RH/tables/contrat/listeContrat.html",{'contrats':contrats})

def ajouterContrat(request):
    if request.method == 'POST':
        form = ContratForm(request.POST)
        if form.is_valid():
            form.save()
            form = ContratForm()
            return render(request,'pages/RH/tables/contrat/ajouterContrat.html',{'form':form})
    else:
        form = ContratForm()
    return render(request,'pages/RH/tables/contrat/ajouterContrat.html',{'form':form})

def modifierContrat(request,pk):
    contrat = Contrat.objects.get(id=pk)
    if request.method == 'POST':
        form = ContratForm(request.POST,instance=contrat)
        if form.is_valid():
            form.save()
            return redirect("listeContrat")
    else:
        form = ContratForm(instance=contrat)
    return render(request,'pages/RH/tables/contrat/modifierContrat.html',{'form':form})

def supprimerContrat(request,pk):
    contrat = Contrat.objects.get(id=pk)
    if request.method == 'POST':
        contrat.delete()
        return redirect('listeContrat')
    else:
        form = ContratForm(instance=contrat)
    return render(request,'pages/RH/tables/contrat/supprimerContrat.html',{'form':form})
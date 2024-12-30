from django.shortcuts import render,redirect
from ..app.models import Objectif
from .forms import ObjectifForm

# Create your views here.

def listeObjectif(request):
    objectifs = Objectif.objects.all()
    return render(request,"pages/RH/tables/objectif/listeObjectif.html",{'objectifs':objectifs})

def ajouterObjectif(request):
    if request.method == 'POST':
        form = ObjectifForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeObjectif')
    else:
        form = ObjectifForm()
    return render(request,"pages/RH/tables/objectif/ajouterObjectif.html",{'form':form})

def modifierObjectif(request,pk):
    objectif = Objectif.objects.get(id=pk)
    if request.method == 'POST':
        form = ObjectifForm(request.POST,instance=objectif)
        if form.is_valid():
            form.save()
            return redirect('listeObjectif')
    else:
        form = ObjectifForm(instance=objectif)
    return render(request,'pages/RH/tables/objectif/modifierObjectif.html',{'form':form})

def supprimerObjectif(request,pk):
    objectif = Objectif.objects.get(id=pk)
    if request.method == 'POST':
        objectif.delete()
        return redirect('listeObjectif')
    else:
        form = ObjectifForm(instance=objectif)
    return render(request,'pages/RH/tables/objectif/supprimerObjectif.html',{'form':form})
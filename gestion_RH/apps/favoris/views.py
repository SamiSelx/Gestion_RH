from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.app.models import Fonctionnalite
from .forms import FonctionnaliteForm
from django.contrib.auth.decorators import login_required

# CRUD for Fonctionnalites
def listeFonctionnalites(request):
    fonctionnalites = Fonctionnalite.objects.all()
    return render(request, 'pages/fonctionnalite/listeFonctionnalites.html', {'fonctionnalites': fonctionnalites})

def ajouterFonctionnalite(request):
    if request.method == 'POST':
        form = FonctionnaliteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeFonctionnalites')
    else:
        form = FonctionnaliteForm()
    return render(request, 'pages/fonctionnalite/ajouter_fonctionnalite.html', {'form': form})

def supprimerFonctionnalite(request, pk):
    fonctionnalite = get_object_or_404(Fonctionnalite, id=pk)
    if request.method == 'POST':
        fonctionnalite.delete()
        return redirect('listeFonctionnalites')
    return render(request, 'pages/fonctionnalite/supprimer_fonctionnalite.html', {'fonctionnalite': fonctionnalite})

def ajouterAuxFavoris(request, pk):
    fonctionnalite = get_object_or_404(Fonctionnalite, id=pk)
    fonctionnalite.favoris = True
    fonctionnalite.save()
    messages.success(request, "La fonctionnalité a été ajouté  aux favoris.")
    return redirect('listeFonctionnalites')  

def retirerDesFavoris(request, pk):
    fonctionnalite = get_object_or_404(Fonctionnalite, id=pk)
    fonctionnalite.favoris = False
    fonctionnalite.save()
    messages.success(request, "La fonctionnalité a été retirer aux favoris.")
    return redirect('listeFonctionnalites')  

def favoris_view(request):
    favoris_list = Fonctionnalite.objects.filter(favoris=True)  
    return render(request, 'base.html', {'favoris_list': favoris_list})
from django.shortcuts import render, redirect, get_object_or_404
from apps.app.models import Fonctionnalite, Favoris, Employe
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

# Manage Favoris
# @login_required
def ajouterAuxFavoris(request, pk):
    fonctionnalite = get_object_or_404(Fonctionnalite, id=pk)
    employe = Employe.objects.get(user=request.user)

    # Check if already in favoris
    if not Favoris.objects.filter(code_employe=employe, code_fonctionnalite=fonctionnalite).exists():
        Favoris.objects.create(code_employe=employe, code_fonctionnalite=fonctionnalite)
    return redirect('listeFonctionnalites')

# @login_required
def supprimerDesFavoris(request, pk):
    fonctionnalite = get_object_or_404(Fonctionnalite, id=pk)
    employe = get_object_or_404(Employe, user=request.user)

    # Remove if exists
    Favoris.objects.filter(code_employe=employe, code_fonctionnalite=fonctionnalite).delete()
    return redirect('listeFonctionnalites')

# Favoris list
# @login_required
def listeFavoris(request):
    employe = get_object_or_404(Employe, user=request.user)
    favoris = Favoris.objects.filter(code_employe=employe)
    
    fonctionnalites_in_favoris = [fav.code_fonctionnalite for fav in favoris]

    return render(request, 'pages/fonctionnalite/liste_favoris.html', {
        'favoris': favoris,
        'fonctionnalites_in_favoris': fonctionnalites_in_favoris
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import constants as messages
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

def ajouterAuxFavoris(request, pk):
    fonctionnalite = get_object_or_404(Fonctionnalite, id=pk)

    # Check if already in favoris
    if not Favoris.objects.filter(code_employe=employe, code_fonctionnalite=fonctionnalite).exists():
        Favoris.objects.create(code_employe=employe, code_fonctionnalite=fonctionnalite)
    return redirect('listeFonctionnalites')

def supprimerDesFavoris(request, pk):
    employe = request.user.employes.first()
    fonctionnalite = get_object_or_404(Fonctionnalite, id=pk)
    
    favorite = Favoris.objects.filter(code_employe=employe, code_fonctionnalite=fonctionnalite)
    if favorite.exists():
        favorite.delete()
        messages.success(request, "Fonctionnalité retirée des favoris.")
    else:
        messages.warning(request, "Cette fonctionnalité n'est pas dans vos favoris.")
    
    return redirect('liste_fonctionnalites')

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
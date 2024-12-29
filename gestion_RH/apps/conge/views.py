from django.shortcuts import render, get_object_or_404, redirect
from ..app.models import Conge
from .forms import CongeForm

# Liste des congés
def liste_conges(request):
    conges = Conge.objects.all()
    return render(request, 'pages/RH/tables/conge/liste_conges.html', {'conges': conges})

# Créer un congé
def creer_conge(request):
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():  # Vérifie si les données sont valides
            form.save()  # Sauvegarde le formulaire dans la base de données
            return redirect('liste_conges')  # Redirige vers la liste des congés
    else:
        form = CongeForm()  # Affiche un formulaire vide
        return render(request, 'pages/RH/tables/conge/creer_conge.html', {'form': form})


# Mettre à jour un congé
def modifier_conge(request, id):
    conge = get_object_or_404(Conge, id=id)
    if request.method == 'POST':
        form = CongeForm(request.POST, instance=conge)
        if form.is_valid():
            form.save()
            return redirect('liste_conges')
    else:
        form = CongeForm(instance=conge)
    return render(request, 'pages/RH/tables/conge/modifier_conge.html', {'form': form})

# Supprimer un congé
def supprimer_conge(request, id):
    conge = get_object_or_404(Conge, id=id)
    if request.method == 'POST':
        conge.delete()
        return redirect('liste_conges')
    return render(request, 'pages/RH/tables/conge/supprimer_conge.html', {'conge': conge})

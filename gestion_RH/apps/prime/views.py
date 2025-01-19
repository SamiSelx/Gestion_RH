from django.shortcuts import render,redirect,get_object_or_404
from ..app.models import Prime
from .forms import PrimeForm

# Create your views here.

def liste_primes(request):
    primes = Prime.objects.all()
    return render(request, 'pages/RH/prime/liste_primes.html', {'primes': primes})

# Créer un congé
def creer_prime(request):
    if request.method == 'POST':
        form = PrimeForm(request.POST)
        if form.is_valid():  # Vérifie si les données sont valides
            form.save()  # Sauvegarde le formulaire dans la base de données
            return redirect('liste_primes')  # Redirige vers la liste des congés
    else:
        form = PrimeForm()  # Affiche un formulaire vide
    return render(request, 'pages/RH/prime/creer_prime.html', {'form': form})


# Mettre à jour un congé
def modifier_prime(request, id):
    prime = get_object_or_404(Prime, id=id)
    if request.method == 'POST':
        form = PrimeForm(request.POST, instance=prime)
        if form.is_valid():
            form.save()
            return redirect('liste_primes')
    else:
        form = PrimeForm(instance=prime)
    return render(request, 'pages/RH/prime/modifier_prime.html', {'form': form})

# Supprimer un congé
def supprimer_prime(request, id):
    prime = get_object_or_404(Prime, id=id)
    if request.method == 'POST':
        prime.delete()
        return redirect('liste_primes')
    return render(request, 'pages/RH/prime/supprimer_prime.html', {'prime': prime})
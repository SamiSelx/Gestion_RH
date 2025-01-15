from django.shortcuts import render, get_object_or_404, redirect
from ..app.models import Conge,DemandeConge,Employe
from .forms import CongeForm,DemandeCongeForm,CongeFilterForm
from django.contrib import messages
from datetime import date

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

def demandeConge(request):
    employe = get_object_or_404(Employe, id=request.user.employe.id)

    if employe.solde_annuel <=0 and request.POST['code_conge'] == 1: ## code conge = 1 <=> congé annuel
        messages.error(request,f"{employe.nomE} pas de solde annuel suffisant")
    if request.method == 'POST':
        form = DemandeCongeForm(request.POST,employe_id=employe.id)
        if form.is_valid():
            form.save()
            return redirect('employePage')
    else:
        form = DemandeCongeForm()
    return render(request,'pages/Employe/conge/demandeConge.html',{'form':form})

def listeCongeEmploye(request):
    conges = DemandeConge.objects.all().order_by('date_debut')
    sort_by_date = request.GET.get('sort_by_date', None)
    if sort_by_date == 'asc':
        conges = conges.order_by('date_debut')
    elif sort_by_date == 'desc':
        conges = conges.order_by('-date_debut')
    form = CongeFilterForm(request.GET)
    if form.is_valid():
        employe = form.cleaned_data.get('employe')
        type_conge = form.cleaned_data.get('type_conge')
        date_debut_from = form.cleaned_data.get('date_debut_from')
        date_debut_to = form.cleaned_data.get('date_debut_to')

        if employe:
            conges = conges.filter(code_employe=employe)
        if type_conge:
            conges = conges.filter(code_conge=type_conge)
        if date_debut_from:
            conges = conges.filter(date_debut__gte=date_debut_from)
        if date_debut_to:
            conges = conges.filter(date_debut__lte=date_debut_to)
    for conge in conges:
        conge.jours_restants = (conge.date_fin - date.today()).days + 1
        conge.jours_utilises =  (date.today() - conge.date_debut).days + 1

    return render(request,'pages/rh/conge/listeCongeEmploye.html',{'conges':conges,'form':form})

def approveCongeEmploye(request,id):
    try:
        if request.method == 'POST':
            conge = get_object_or_404(DemandeConge,id=id)
            if conge.status == 'En attente':
                conge.changeStatus('Approuvé')
                if conge.code_conge.type_conge == "Annuel":
                    conge.mettre_a_jour_solde()
            else: 
                messages.error(request, 'conge is already approved.')
                return render(request,'pages/rh/conge/approveCongeEmploye.html')
            return redirect('listeCongeEmploye')
        else:
            return render(request,'pages/rh/conge/approveCongeEmploye.html')
    except ValueError as e:
        messages.error(request,e)
        return render(request,'pages/rh/conge/approveCongeEmploye.html')
    
def termineCongeEmploye(request,id):
    if request.method == 'POST':
        try:
            conge = get_object_or_404(DemandeConge, id=id)
            if conge.status == "Terminé":
                raise ValueError("L'employé deja terminé son congé")
            if conge.code_conge.type_conge == "Annuel":
                conge.cloturer_conge()
            return redirect('listeCongeEmploye')
        except ValueError as e:
            messages.error(request, e)
            return render(request,'pages/rh/conge/termineCongeEmploye.html')
    else: 
        return render(request,'pages/rh/conge/termineCongeEmploye.html')
    
def supprimerDemandeConge(request,id):
    conge = get_object_or_404(DemandeConge, id=id)
    if request.method == 'POST':
        conge.delete()
        return redirect('listeCongeEmploye')
    return render(request, 'pages/rh/conge/supprimerCongeEmploye.html', {'conge': conge})
        
from apps.app.models import Candidature ,Offre_employe
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CandidatureForm , EntretienForm , CandidatureStatusForm

def postuler_offre(request, offre_id):
    offre = get_object_or_404(Offre_employe, id=offre_id)
    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES, candidat_id = request.user.candidat.id)  
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.offre = offre
            candidature.save()
            return redirect('liste_offre_employe')
    else:
        form = CandidatureForm()
    return render(request, 'pages/recruitment/postuler_offre.html', {'form': form, 'offre': offre})

def liste_candidatures(request):
    candidatures = Candidature.objects.select_related('candidat', 'offre').all()
    return render(request, 'pages/rh/tables/gestionCandidature/liste_candidatures.html', {'candidatures': candidatures})


def planifier_entretien(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)
    if request.method == 'POST':
        form = EntretienForm(request.POST)
        if form.is_valid():
            entretien = form.save(commit=False)
            entretien.candidature = candidature
            entretien.save()
            return redirect('liste_candidatures')
    else:
        form = EntretienForm()
    return render(request, 'pages/recruitment/planifier_entretien.html', {'form': form, 'candidature': candidature})


def modifier_statut(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)
    if request.method == 'POST':
        form = CandidatureStatusForm(request.POST, instance=candidature)
        if form.is_valid():
            form.save()
            return redirect('liste_candidatures') 
    else:
        form = CandidatureStatusForm(instance=candidature)
    return render(request, 'pages/rh/tables/gestionCandidature/modifier_statut.html', {'form': form, 'candidature': candidature})


def candidature_detail(request, id): 
    candidature = get_object_or_404(Candidature, id=id) 
    return render(request, 'pages/rh/tables/Employe/employe_detail.html', {'candidature': candidature})

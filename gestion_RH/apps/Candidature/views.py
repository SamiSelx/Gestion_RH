from apps.app.models import Candidature ,Offre_employe
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CandidatureForm , EntretienForm , CandidatureStatusForm 
from django.db.models import Count, F
from django.db.models.functions import TruncMonth
from datetime import date, timedelta

def success_page(request):
    return render(request, 'pages/recruitment/successPage.html')

def postuler_offre(request, offre_id):
    offre = get_object_or_404(Offre_employe, id=offre_id)
    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES, candidat_id = request.user.candidat.id)  
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.offre = offre
            candidature.save()
            return redirect('successPage')
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
    return render(request, 'pages/rh/tables/candidat/detail_candidat.html', {'candidature': candidature})





def analyse_recrutement(request):
    # Calculer les périodes (12 mois précédents)
    today = date.today()
    start_date = today - timedelta(days=365)

    # Taux d'évolution des nouveaux recrutés
    recrutements_par_mois = (
        Candidature.objects.filter(date_soumission__gte=start_date)
        .annotate(month=TruncMonth('date_soumission'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Taux d'évolution des offres publiées
    offres_par_mois = (
        Offre_employe.objects.filter(date_posted__gte=start_date)
        .annotate(month=TruncMonth('date_posted'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Formater les données pour les graphiques
    recrutements_data = {
        'months': [item['month'].strftime('%Y-%m') for item in recrutements_par_mois],
        'counts': [item['count'] for item in recrutements_par_mois],
    }
    offres_data = {
        'months': [item['month'].strftime('%Y-%m') for item in offres_par_mois],
        'counts': [item['count'] for item in offres_par_mois],
    }

    context = {
        'recrutements_data': recrutements_data,
        'offres_data': offres_data,
    }

    return render(request, 'pages/RH/analyse/analyse_recrutement.html', context)

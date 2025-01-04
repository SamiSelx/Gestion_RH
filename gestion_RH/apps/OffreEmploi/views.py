# apps/Formation/views.py

from django.shortcuts import render, get_object_or_404, redirect
from apps.app.models import Offre_employe
from .forms import OffreEmployeForm

def create_offre_employe(request):
    if request.method == 'POST':
        form = OffreEmployeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_offre_employe')  
    else:
        form = OffreEmployeForm()
    return render(request, 'pages/rh/tables/offre_employe/create_offre_employe.html', {'form': form})

def liste_offre_employe(request):
    offres = Offre_employe.objects.all()
    return render(request, 'pages/rh/tables/offre_employe/liste_offre_employe.html', {'offres': offres})

def update_offre_employe(request, pk):
    offre = get_object_or_404(Offre_employe, pk=pk)
    if request.method == 'POST':
        form = OffreEmployeForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            return redirect('liste_offre_employe')
    else:
        form = OffreEmployeForm(instance=offre)
    return render(request, 'pages/rh/tables/offre_employe/update_offre_employe.html', {'form': form})

def delete_offre_employe(request, pk):
    offre = get_object_or_404(Offre_employe, pk=pk)
    if request.method == 'POST':
        offre.delete()
        return redirect('liste_offre_employe')
    return render(request, 'pages/rh/tables/offre_employe/delete_offre_employe.html', {'offre': offre})

def offreEmploye_detail(request, id):
    offre = get_object_or_404(Offre_employe, id=id) 
    return render(request, 'pages/rh/tables/offre_employe/offreEmploye_detail.html', {'offre': offre})

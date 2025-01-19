from django.shortcuts import render, get_object_or_404, redirect
from apps.app.models import Employe
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse
from .forms import EmployeForm

def employe_list(request):
    employes_list = Employe.objects.all()
    paginator = Paginator(employes_list, 10)

    page_number = request.GET.get('page')
    employes = paginator.get_page(page_number)
    return render(request, 'pages/rh/tables/Employe/employe_list.html', {'employes': employes})


def employe_detail(request, id): 
    employe = get_object_or_404(Employe, id=id) 
    return render(request, 'pages/rh/tables/Employe/employe_detail.html', {'employe': employe})


def employe_create(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employe_list')
    else:
        form = EmployeForm()
    return render(request, 'pages/rh/tables/Employe/employe_form.html', {'form': form})


def employe_update(request, id): 
    employe = get_object_or_404(Employe, id=id) 
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('employe_list')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'pages/rh/tables/Employe/employe_form.html', {'form': form})


def employe_delete(request, id):  
    employe = get_object_or_404(Employe, id=id)  
    if request.method == 'POST':
        employe.delete()
        return redirect('employe_list')
    return render(request, 'pages/rh/tables/Employe/employe_confirm_delete.html', {'employe': employe})

def export_employe_csv(request, employe_id):
    employe = Employe.objects.get(id=employe_id)
  
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="employe_{employe.id}_details.csv"'
   
    writer = csv.writer(response)
    
   
    writer.writerow([
        'Employee ID', 'Name', 'Gender', 'Date of Birth', 'Date of Hire', 
        'Address', 'Service', 'Competences', 'Formations', 'Objectifs', 'Conges'
    ])

   
    competences = ", ".join([competence.nom_competence for competence in employe.competences.all()])
    formations = ", ".join([formation.titre_formation for formation in employe.formations.all()])
    objectifs = ", ".join([f"{objectif.description_objectif} (Deadline: {objectif.date_limite})" for objectif in employe.objectifs.all()])
    conges = ", ".join([
        f"{conge.type_conge} (Start: {conge.date_debut}, End: {conge.date_fin}, Desc: {conge.description or 'No description'})"
        for conge in employe.conges.all()
    ])

    
    writer.writerow([
        employe.id,
        f"{employe.nomE} {employe.prenomE}",
        employe.get_gender_display(),
        employe.date_naissance_E,
        employe.date_embauche_E,
        employe.adresse_E,
        employe.code_service.description_service,
        competences,
        formations,
        objectifs,
        conges
    ])

    return response

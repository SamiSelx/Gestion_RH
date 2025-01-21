from django.shortcuts import render,redirect, get_object_or_404
from apps.app.models import Contrat
from .forms import ContratForm
from django.contrib import messages
from datetime import date
import csv
from django.http import HttpResponse,FileResponse
from django.template.loader import render_to_string
from django.utils import timezone

## PDF Library
from django.http import FileResponse,HttpResponse
import io
from xhtml2pdf import pisa

def afficheContrat(request):
    search_query = request.GET.get('search', '')  

    if search_query:
        
        contrats = Contrat.objects.filter(code_employe__nomE__icontains=search_query)
        if not contrats:
            messages.info(request, "Aucun contrat trouvé pour cet employé.")
    else:
        # contrats = Contrat.objects.all()
        contrats = Contrat.objects.filter(archive=False)
        
    return render(request,"pages/RH/tables/contrat/listeContrat.html",{'contrats':contrats})

# def afficheContrat(request):
#     contrats = Contrat.objects.all()
#     return render(request,"pages/RH/tables/contrat/listeContrat.html",{'contrats':contrats})

def ajouterContrat(request):
    if request.method == 'POST':
        form = ContratForm(request.POST)
        if form.is_valid():
            contrat = form.save()
            if form.cleaned_data['date_fin_contrat'] == date.today():
                contrat.etat = 'non-actif'
                contrat.save()

            messages.success(request, "Le contrat a été ajouté avec succès.")
            return redirect('listeContrat')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = ContratForm()
    return render(request, 'pages/RH/tables/contrat/ajouterContrat.html', {'form': form})

def modifierContrat(request, pk):
    contrat = Contrat.objects.get(id=pk)
    
    if request.method == 'POST':
        form = ContratForm(request.POST, instance=contrat)
        if form.is_valid():
            if form.cleaned_data['date_fin_contrat'] == date.today():
                contrat.etat = 'non-actif'
                contrat.save()
            if form.cleaned_data['date_fin_contrat'] != date.today():
                contrat.etat = 'actif'
                contrat.save()

            form.save()  # Save the form data
            return redirect("listeContrat")
    else:
        form = ContratForm(instance=contrat)

    return render(request, 'pages/RH/tables/contrat/modifierContrat.html', {'form': form})

def archiveContrat(request):
    contrats = Contrat.objects.filter(archive=True)
    return render(request, "pages/RH/tables/contrat/archiveContrat.html", {'contrats': contrats})

def supprimerContrat(request, pk):
    contrat = get_object_or_404(Contrat, pk=pk) 
  
    contrat.archive = True
    contrat.save()
    messages.success(request, f"Le contrat {contrat.type_contrat} a été archivé avec succès.")
    return redirect('archiveContrat') 

def contrat_detail(request, id): 
    contrat = get_object_or_404(Contrat, id=id) 
    return render(request, 'pages/rh/tables/contrat/contrat_detail.html', {'contrat': contrat})

def contrat_detail_EMP(request): 
    contrat = get_object_or_404(Contrat, code_employe=request.user.employe.id)
    return render(request, 'pages/Employe/contrat/contrat_detail_EMP.html', {'contrat': contrat})

def check_contrat_expiration(request):
    today = date.today()
    # Fetch active contracts that expire today
    contrats_a_expirer = Contrat.objects.filter(date_fin_contrat=today, etat='actif')

    for contrat in contrats_a_expirer:
        # Check if the current user matches the contract's employee
        if request.user == contrat.code_employe:
            messages.warning(
                request, 
                f"Votre contrat avec {contrat.code_employe.nomE} expire aujourd'hui ({contrat.date_fin_contrat})."
            )
        
        
        contrat.etat = 'non-actif'
        contrat.save()

    return redirect('listeContrat')
    

def export_contrat_csv(request, contrat_id):
    contrat = Contrat.objects.get(id=contrat_id)
  
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="contrat_{contrat.id}_details.csv"'
   
    
    writer = csv.writer(response)
    
   
    writer.writerow([
        'Contrat ID', 'Type de Contrat', 'Date de Début', 'Date de Fin', 'Salaire', 'État', 'Employé'
    ])

    
    writer.writerow([
        contrat.id,
        contrat.get_type_contrat_display(),  
        contrat.date_debut_contrat,
        contrat.date_fin_contrat,
        contrat.salaire,
        contrat.etat,
        f"{contrat.code_employe.nomE} {contrat.code_employe.prenomE}"  
    ])

    return response



def fiche_journal_contrats(request):
    service_filter = request.GET.get('service', '')
    date_debut_filter = request.GET.get('date_debut', '')
    date_fin_filter = request.GET.get('date_fin', '')
    type_filter = request.GET.get('type', '')

    
    contrats = Contrat.objects.filter(archive=False)

    if service_filter:
        contrats = contrats.filter(code_employe__code_service__description_service=service_filter)
    
    if date_debut_filter and date_fin_filter:
        contrats = contrats.filter(
            date_debut_contrat__gte=date_debut_filter, 
            date_fin_contrat__lte=date_fin_filter
        )
    
    if type_filter:
        contrats = contrats.filter(type_contrat=type_filter)

    if not contrats:
        messages.info(request, "Aucun contrat ne correspond à vos critères de recherche.")

    return render(request, 'pages/RH/tables/contrat/listeFiltrer.html', {'contrats': contrats})

def generate_fiche_de_contrat(request,contrat_id):
    contrat = Contrat.objects.get(id=contrat_id)
    html_content = render_to_string('fiche_de_contrat.html', {
        'employe': contrat.code_employe,
        'contrat': contrat,
        'date': timezone.now().strftime('%Y-%m-%d')
    })

    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=400)
    
    # Move the cursor to the beginning of the BytesIO buffer
    pdf_buffer.seek(0)
    return FileResponse(pdf_buffer, as_attachment=True, filename=f'fiche_de_contrat.pdf')
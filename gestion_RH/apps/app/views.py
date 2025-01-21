from django.shortcuts import render,redirect
from .models import Offre_employe
# from django.contrib.auth.decorators import login_required
from .models import Employe,Contrat
from django.db.models import Count
import json
from datetime import date
from django.utils.text import Truncator


# @login_required
def home(request):
    # k = 20
    # for i in range(5):
    #     emp = Employe.objects.get(pk = k)
    #     if emp:
    #         Contrat.objects.create(
    #             type_contrat= "Stagiaire",
    #             date_debut_contrat = "2018-10-4",
    #             date_fin_contrat = "2018-12-04",
    #             salaire = 600000,
    #             etat = "non-actif",
    #             code_employe = emp,
    #         )
    #     k = k-1

    offres = Offre_employe.objects.all()
    truncated_offres = []

    for offre in offres:
        truncated_description = Truncator(offre.description).chars(100)
        truncated_offres.append({
            'offre': offre,
            'truncated_description': truncated_description
        })
    return render(request,"pages/home/index.html",{'offres': truncated_offres})


# Handle Errors----------

def custom_404(request, exception):
    return render(request, '404.html', status=404)

# For Page RH ------------
def RhTables(request):
    return render(request,"pages/RH/tables/tables.html")

def RhRedirect(request):
    return redirect('dashboard')

def employeeAnalyses(request):
    total_employees = Employe.objects.count()
    diversity_gender = Employe.objects.values('gender').annotate(count=Count('gender'))
    diversity_gender_list = list(diversity_gender)
    diversity_gender_json = json.dumps(diversity_gender_list)
    contract_data= Contrat.objects.values('type_contrat').annotate(count=Count('type_contrat'))

    contract_data_list = list(contract_data)

    contract_data_json = json.dumps(contract_data_list)
    today = date.today()
    age_distribution = [
        {'range': '<25', 'count': Employe.objects.filter(date_naissance_E__gte=today.replace(year=today.year - 25)).count()},
        {'range': '25-35', 'count': Employe.objects.filter(
            date_naissance_E__lt=today.replace(year=today.year - 25),
            date_naissance_E__gte=today.replace(year=today.year - 35)
        ).count()},
        {'range': '35-50', 'count': Employe.objects.filter(
            date_naissance_E__lt=today.replace(year=today.year - 35),
            date_naissance_E__gte=today.replace(year=today.year - 50)
        ).count()},
        {'range': '>50', 'count': Employe.objects.filter(date_naissance_E__lt=today.replace(year=today.year - 50)).count()},
    ]
    seniority_distribution = [
        {'range': '<5 years', 'count': Employe.objects.filter(date_embauche_E__gte=today.replace(year=today.year - 5)).count()},
        {'range': '5-10 years', 'count': Employe.objects.filter(
            date_embauche_E__lt=today.replace(year=today.year - 5),
            date_embauche_E__gte=today.replace(year=today.year - 10)
        ).count()},
        {'range': '>10 years', 'count': Employe.objects.filter(date_embauche_E__lt=today.replace(year=today.year - 10)).count()},
    ]
    
    context = {
        'total_employees': total_employees,
        'diversity_gender': diversity_gender_json,
        'contract_data':contract_data_json,
        'age_distribution': json.dumps(age_distribution),
        'seniority_distribution': json.dumps(seniority_distribution),
    }
    nombre_employes = Employe.objects.count()
    homme_employe = Employe.objects.filter(gender='M').count()
    femelle_employe = Employe.objects.filter(gender='F').count()
    return render(request,'pages/rh/analyse/employeAnalyses.html',{'context':context,'nombre_employes':nombre_employes,'homme_employe':homme_employe,'femelle_employe':femelle_employe})
#-------------------------

# For Page Employee ------------
def employe(request):
    return redirect('informationPersonnel')

def informationPersonnel(request):
    return render(request,'pages/employe/information/informationPersonnel.html')
 


#page Manager-------------------
def Manager(request):
    return redirect('informationPersonnelM')

def informationPersonnelM(request):
    return render(request,'pages/Manager/information/informationPersonnelM.html')
 

# page RH-------------------

def dashboard(request):
    total_employees = Employe.objects.count()
    diversity_gender = Employe.objects.values('gender').annotate(count=Count('gender'))
    diversity_gender_list = list(diversity_gender)
    diversity_gender_json = json.dumps(diversity_gender_list)
    contract_data= Contrat.objects.values('type_contrat').annotate(count=Count('type_contrat'))

    contract_data_list = list(contract_data)

    contract_data_json = json.dumps(contract_data_list)
    today = date.today()
    age_distribution = [
        {'range': '<25', 'count': Employe.objects.filter(date_naissance_E__gte=today.replace(year=today.year - 25)).count()},
        {'range': '25-35', 'count': Employe.objects.filter(
            date_naissance_E__lt=today.replace(year=today.year - 25),
            date_naissance_E__gte=today.replace(year=today.year - 35)
        ).count()},
        {'range': '35-50', 'count': Employe.objects.filter(
            date_naissance_E__lt=today.replace(year=today.year - 35),
            date_naissance_E__gte=today.replace(year=today.year - 50)
        ).count()},
        {'range': '>50', 'count': Employe.objects.filter(date_naissance_E__lt=today.replace(year=today.year - 50)).count()},
    ]

    anciennete_distribution = [
        {'range': '<5 years', 'count': Employe.objects.filter(date_embauche_E__gte=today.replace(year=today.year - 5)).count()},
        {'range': '5-10 years', 'count': Employe.objects.filter(
            date_embauche_E__lt=today.replace(year=today.year - 5),
            date_embauche_E__gte=today.replace(year=today.year - 10)
        ).count()},
        {'range': '>10 years', 'count': Employe.objects.filter(date_embauche_E__lt=today.replace(year=today.year - 10)).count()},
    ]
    
    context = {
        'total_employees': total_employees,
        'diversity_gender': diversity_gender_json,
        'contract_data':contract_data_json,
        'age_distribution': json.dumps(age_distribution),
        'seniority_distribution': json.dumps(anciennete_distribution),
    }
    nombre_employes = Employe.objects.count()
    homme_employe = Employe.objects.filter(gender='M').count()
    femelle_employe = Employe.objects.filter(gender='F').count()
    return render(request,'pages/rh/dashboard/dashboard.html',{'context':context,'nombre_employes':nombre_employes,'homme_employe':homme_employe,'femelle_employe':femelle_employe})
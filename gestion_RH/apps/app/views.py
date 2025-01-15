from django.shortcuts import render,redirect
from .models import Offre_employe
# from django.contrib.auth.decorators import login_required
from .models import Employe,Contrat
from django.db.models import Count
import json
from datetime import date

# @login_required
def home(request):
    offres = Offre_employe.objects.all()
    return render(request,"pages/home/index.html",{'offres': offres})

# For Page RH ------------
def RhTables(request):
    return render(request,"pages/RH/tables/tables.html")

def RhRedirect(request):
    return redirect('tables')

def employeeAnalyses(request):
    total_employees = Employe.objects.count()
    diversity_gender = Employe.objects.values('gender').annotate(count=Count('gender'))
    # top_performers = Employe.objects.filter(performance__gte=4).order_by('-performance')[:10]
    diversity_gender_list = list(diversity_gender)
    diversity_gender_json = json.dumps(diversity_gender_list)
    # Query data for employees grouped by contract type
    contract_data= Contrat.objects.values('type_contrat').annotate(count=Count('type_contrat'))

    # Convert QuerySet to a list of dictionaries
    contract_data_list = list(contract_data)

    # Serialize the data into JSON
    contract_data_json = json.dumps(contract_data_list)
        # Age distribution (e.g., <25, 25-35, 35-50, >50)
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
    # Seniority distribution (e.g., <5 years, 5-10 years, >10 years)
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
        # 'top_performers': top_performers,
    }
    return render(request,'pages/rh/analyse/employeAnalyses.html',{'context':context})
#-------------------------

# For Page Employee ------------
def employe(request):
    # return render(request,'pages/employe/employePage.html')
    return redirect('informationPersonnel')

def informationPersonnel(request):
    return render(request,'pages/employe/information/informationPersonnel.html')
 


#page Manager-------------------
def Manager(request):
    return redirect('informationPersonnelM')

def informationPersonnelM(request):
    return render(request,'pages/Manager/information/informationPersonnelM.html')
 

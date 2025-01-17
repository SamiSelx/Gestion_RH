from django.shortcuts import render,redirect,get_object_or_404
from ..app.models import Employe,Absence,DemandeAvanceSalaire,Prime,FicheDePaieS
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import date
from .forms import DemandeAvanceSalaireForm
from datetime import date, timedelta
from django.utils import timezone
from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from decimal import Decimal
from django.conf import settings

## PDF Library
from django.http import FileResponse,HttpResponse
import io
from xhtml2pdf import pisa

# Create your views here.

def employeList(request):
    employes = Employe.objects.all()
    employes_list = Employe.objects.all()
    paginator = Paginator(employes_list, 10)

    page_number = request.GET.get('page')
    employes = paginator.get_page(page_number)
    today = date.today()
    for employe in employes:
            absence = Absence.objects.filter(
                code_employe = employe.id,
                date_absence__day=today.day,
                date_absence__month=today.month,
                date_absence__year=today.year,
            ).first()
            if absence:
                employe.absence = "OUI"
            else: 
                 employe.absence = "NON"
    # if request.method == "POST":
    #     for employe in employes:
    #         is_absent = request.POST.get(f'absence_{employe.id}')
    #         print(is_absent)
    #         if not is_absent:
    #             if not Absence.objects.filter(code_employe=employe.id,date_absence__day=today.day,date_absence__month=today.month,date_absence__year=today.year).exists():
    #                 Absence.objects.create(code_employe=employe, date_absence=today)
    #         else:
    #             Absence.objects.filter(code_employe=employe.id, date_absence__day=today.day,date_absence__month=today.month,date_absence__year=today.year).delete()
            
    #     return redirect('absenceEmploye') 

    return render(request,'pages/rh/absence/listeEmploye.html',{'employes':employes})

def marqueAbsence(request,employeId):
        employe = Employe.objects.get(pk=employeId)
        # form = AbsenceForm(request.POST,employe_id=employeId)
        # absence = Absence.objects.create()   
        today = date.today()
        today_month = today.month
        today_year = today.year
        today_day = today.day

        deja_absent = Absence.objects.filter(
            code_employe=employe.id,
            date_absence__day=today_day,
            date_absence__month=today_month,
            date_absence__year=today_year,
        ).exists()
        if deja_absent:
            messages.error(request,"l'emloyé est deja absent")
            Absence.objects.filter(code_employe=employe.id,
                                    date_absence__day=today.day,
                                    date_absence__month=today.month,
                                    date_absence__year=today.year).delete()
            return redirect('absenceEmploye')
        
        Absence.objects.create(code_employe=employe,date_absence=today)
        messages.success(request,f'Employe {employe.nomE} est Absence')
        return redirect('absenceEmploye')

def absenceListe(request):
    today = date.today()
    month = request.GET.get('month',today.month)
    day = request.GET.get('day')

    absences = Absence.objects.all().order_by('code_employe')

    if month:
        absences = Absence.objects.filter(date_absence__month=month).order_by('code_employe')
    if day:
        absences = Absence.objects.filter(date_absence__day=day).order_by('code_employe')
        
    return render(request, 'pages/rh/absence/absenceListe.html', {
        'absences': absences,
        'month': month,
        'day': day
    })

def listeEmployeSalaire(request):
    employes = Employe.objects.all()
    
    today = date.today()
    if request.method == 'POST':
        employe = Employe.objects.get(pk=request.POST.get('employeId'))
        fiche_de_paie = FicheDePaieS.objects.filter(
            employe=employe,
            month__year=today.year,
            month__month=today.month
        ).first()
        if fiche_de_paie:
            messages.add_message(request,messages.ERROR,'the salairy already calculed')
            return redirect('listeEmployeSalaire')
        
        heure_supp = Decimal(request.POST.get('heures_supp'))
        salaire_mensuel = calcule_salaire_mensuel(employe,today.month,today.year,heure_supp)
        FicheDePaieS.objects.get_or_create(
            employe=employe,
            month=today.replace(day=1),
            salaire_mensuel = salaire_mensuel,
            heures_supp = heure_supp,
            defaults={'salaire_base': employe.salaire_base.salaire_base} 
        )
        # for employe in employes:
        #     # salaire = calcule_salaire_mensuel(employe,today.month,today.year)
        #     # employe.salaire = salaire
        #     if employe.id == int(request.POST.get('employeId')):
        #         employe.salaire = salaire_mensuel
    fiche_de_paie = FicheDePaieS.objects.filter(
            month__year=today.year,
            month__month=today.month
        )
    
    return render(request,'pages/rh/salaire/listeEmployeSalaire.html',{'employes':employes,'fiche_de_paie':fiche_de_paie}) 

def employeSalaireDetail(request,code_employe):
     employe = Employe.objects.get(pk=code_employe)
     absences = Absence.objects.filter(code_employe=employe.id)
     primes = Prime.objects.filter(code_employe = employe.id)
     avanceSalaires = DemandeAvanceSalaire.objects.filter(code_employe = code_employe, approuvee = True)
     return render(request,'pages/rh/salaire/employeSalaireDetail.html',{
          'employe':employe,
          'absences':absences,
          'primes':primes,
          'avanceSalaires':avanceSalaires
     })

def calcule_salaire_mensuel(employe, month, year,heure_supp):
    salaire_base = employe.salaire_base.salaire_base
    
    days_in_month = (date(year, month + 1, 1) - timedelta(days=1)).day
    workdays = [d for d in range(1, days_in_month + 1) if date(year, month, d).weekday() in range(5)]
    salaire_quotidien = salaire_base / len(workdays)
    salaire_par_heure = salaire_quotidien / 8
    
    # Check absences in the month
    absences = Absence.objects.filter(code_employe=employe.id, date_absence__month=month, date_absence__year=year).count()
    deduction = absences * salaire_quotidien

    # Calculate primes for the month
    primes = Prime.objects.filter(code_employe=employe.id, date_attribuee__month=month, date_attribuee__year=year)
    total_primes = sum([prime.prime_montant for prime in primes])
    salaireAvances = DemandeAvanceSalaire.objects.filter(code_employe=employe.id,date_demande__month=month,date_demande__year=year)
    total_salaire_avance = sum([salaireAvance.montant for salaireAvance in salaireAvances])
    
    # Final salary
    salaire_mensuel = round(salaire_base - deduction + (salaire_par_heure * heure_supp )+ total_primes - total_salaire_avance,2)
    return salaire_mensuel
## Employe:
def demandeAvanceSalaire(request):
    employe = get_object_or_404(Employe,id=request.user.employe.id)
    form = DemandeAvanceSalaireForm()
    if request.method == 'POST':
        today = date.today()
        ## nombre demande d'avance par an
        nombreDemandeAvance = DemandeAvanceSalaire.objects.filter(code_employe = request.user.employe.id,date_demande__year = today.year).count()
        if nombreDemandeAvance == 2:
             messages.error(request,"Tu as dépasser le nombre de demande, contact RH plus de detaile")
             return render(request,'pages/employe/salaire/demandeAvanceSalaire.html',{'form':form}) 
        form = DemandeAvanceSalaireForm(request.POST,employe_id=employe.id) 
        if form.is_valid():
            form.save()
            return redirect('listeDemandeAvanceSalaire')
    else:
        form = DemandeAvanceSalaireForm()
    return render(request,'pages/employe/salaire/demandeAvanceSalaire.html',{'form':form})

def listeDemandeAvanceSalaire(request):
    demandeEmploye = DemandeAvanceSalaire.objects.filter(code_employe = request.user.employe.id)
    return render(request,'pages/employe/salaire/listeDemandeAvanceSalaire.html',{'demandes':demandeEmploye})

def listeDemandeAvanceSalaireAll(request):
    demandeSalaires = DemandeAvanceSalaire.objects.all()
    return render(request,'pages/rh/salaire_avance/liste_demande_avance.html',{'avances':demandeSalaires})

def approuveeDemandeAvance(request,avanceId):
    if request.method == 'POST':
        avance = DemandeAvanceSalaire.objects.get(pk=avanceId)
        avance.approuvee = not avance.approuvee
        avance.save()
        messages.add_message(request,messages.SUCCESS,'Demande avance salaire est approuvee')
        return redirect('listesAvanceSalaire')
    return redirect('listesAvanceSalaire')

# generate and send fiche de paie

def send_fiche_de_paie(employe):
    if not hasattr(employe, 'user') or employe.user is None:
        raise ValueError("employe n'a pas un compte")
    today = date.today()
    
    # salaire = employe.salaire_base.salaire_base
    primes = Prime.objects.filter(code_employe=employe.id, date_attribuee__month=date.today().month, date_attribuee__year=date.today().year)
    total_prime= sum([prime.prime_montant for prime in primes])
   
    html_content = render_to_string('fiche_de_paie.html', {
        'employe': employe,
        'salaire': calcule_salaire_mensuel(employe,today.month,today.year,0),
        'primes': total_prime,
        'date': timezone.now().strftime('%Y-%m-%d')
    })

    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=400)
    
    # Move the cursor to the beginning of the BytesIO buffer
    pdf_buffer.seek(0)

    # Prepare email
    email = EmailMessage(
        subject="Votre Fiche de Paie",
        body="Veuillez trouver ci-joint votre fiche de paie pour ce mois.",
        from_email=settings.EMAIL_FROM_USER,
        to=[employe.user.email],  # Ensure this is the email of the employee
    )

    # Attach the PDF file to the email (provide the name and content)
    email.attach(f"fiche_de_paie_{employe.id}.pdf", pdf_buffer.read(), "application/pdf")

    # Send email
    email.send()

def send_fiche_de_paie_view(request, code_employe):
    employe = get_object_or_404(Employe, id=code_employe)
    try:
        send_fiche_de_paie(employe)
        messages.success(request, f"Fiche de paie envoyée à {employe.nomE}.")
    except Exception as e:
        messages.error(request, f"Erreur lors de l'envoi: {e}")

    return redirect('listeEmployeSalaire') 

## gestion prime

# def primesEmployes(request):

#     return render(request,'pages/rh/primesEmployes.html')

# def addPrimeEmploye(request,code_employe):
#     employe = get_object_or_404(Employe,id=code_employe)
#     if request.method == 'POST':
        

def generate_fiche_de_paie(request,code_employe):
    today = date.today()
    # Retrieve necessary data
    employe = Employe.objects.get(pk=code_employe)
    # salaire = employe.salaire_base.salaire_base
    primes = Prime.objects.filter(code_employe=employe.id, date_attribuee__month=date.today().month, date_attribuee__year=date.today().year)
    total_prime= sum([prime.prime_montant for prime in primes])
    # employe.salaire = calcule_salaire_mensuel(employe,today.month,today.year)
    fiche_de_paie = FicheDePaieS.objects.filter(
        employe = employe,
        month__year=today.year,
        month__month=today.month
    ).first()
    html_content = render_to_string('fiche_de_paie.html', {
        'employe': employe,
        'salaire': fiche_de_paie.salaire_mensuel,
        'primes': total_prime,
        'heures_supp':fiche_de_paie.heures_supp,
        'date': timezone.now().strftime('%Y-%m-%d')
    })

    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=400)
    
    # Move the cursor to the beginning of the BytesIO buffer
    pdf_buffer.seek(0)
    return FileResponse(pdf_buffer, as_attachment=True, filename=f'fiche_de_paie.pdf')
from django.shortcuts import render,redirect,get_object_or_404
from ..app.models import Employe,Absence,DemandeAvanceSalaire,Prime
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import date
from .forms import DemandeAvanceSalaireForm
from datetime import date, timedelta
from django.utils import timezone
from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from decimal import Decimal

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
        employeUpdate = Employe.objects.get(pk=request.POST.get('employeId'))
        heure_supp = Decimal(request.POST.get('heures_supp'))
        # employe.salaire = calcule_salaire_mensuel(employe,today.month,today.year,heure_supp)
        for employe in employes:
            # salaire = calcule_salaire_mensuel(employe,today.month,today.year)
            # employe.salaire = salaire
            if employe.id == int(request.POST.get('employeId')):
                employe.salaire = calcule_salaire_mensuel(employe,today.month,today.year,heure_supp)


     return render(request,'pages/rh/salaire/listeEmployeSalaire.html',{'employes':employes}) 

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
    # Retrieve necessary data
    salaire = employe.salaire_base.salaire_base
    primes = Prime.objects.filter(code_employe=employe.id, date_attribuee__month=date.today().month, date_attribuee__year=date.today().year) or 0
    total_prime= sum([prime.prime_montant for prime in primes])
   # Render HTML for pay slip
    html_content = render_to_string('fiche_de_paie.html', {
        'employe': employe,
        'salaire': salaire,
        'primes': total_prime,
        'date': timezone.now().strftime('%Y-%m-%d')
    })

    # Generate PDF using WeasyPrint
    # pdf_file = HTML(string=html_content).write_pdf()

    # Prepare email
    # email = EmailMessage(
    #     subject="Votre Fiche de Paie",
    #     body="Veuillez trouver ci-joint votre fiche de paie pour ce mois.",
    #     from_email="yassersellal14@gmail.com",
    #     to=['samifcb14@gmail.com'],
    # )
    # email.attach(f"fiche_de_paie_{employe.id}", 'html_content')

    # Send email
    # email.send()
    subject = 'Hello from Django'
    message = 'This is a test email sent from Django.'
    from_email = 'yassersam1234@outlook.com'  # Same as EMAIL_HOST_USER
    recipient_list = list(['samifcb14@gmail.com'] ) # Replace with recipient's email

    send_mail(subject, message, from_email, recipient_list)

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
        
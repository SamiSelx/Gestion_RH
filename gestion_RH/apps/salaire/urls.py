from django.urls import path
from . import views

urlpatterns = [
    path('rh/absence/',views.employeList,name='absenceEmploye'),
    path('rh/absence/<int:employeId>',views.marqueAbsence,name='marqueAbsence'),
    path('rh/absence/filter/',views.absenceListe,name='absenceListe'),
    path('rh/analyse/absence/',views.analyseAbsence,name='analyseAbsence'),
    path('rh/salaire/',views.listeEmployeSalaire,name='listeEmployeSalaire'),
    path('rh/salaire/<int:code_employe>',views.employeSalaireDetail,name='employeSalaireDetail'),
    path('employe/demandeAvanceSalaire/',views.demandeAvanceSalaire,name='demandeAvanceSalaire'),
    path('employe/demandeAvanceSalaire/liste/',views.listeDemandeAvanceSalaire,name='listeDemandeAvanceSalaire'),
    path('rh/listesAvanceSalaire/',views.listeDemandeAvanceSalaireAll,name='listesAvanceSalaire'),
    path('rh/listesAvanceSalaire/approuvee/<int:avanceId>',views.approuveeDemandeAvance,name='approuveeAvance'),
    path('rh/salaire/<int:code_employe>/send_fiche_de_paie/',views.send_fiche_de_paie_view,name='send_fiche_de_paie'),
    path('rh/salaire/<int:code_employe>/fiche_de_paie/',views.generate_fiche_de_paie,name='fiche_de_paie'),
    # path('rh/prime/add/<int:code_employe>',views.addPrimeEmploye,name='addPrimeEmploye'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('rh/tables/contrat/',views.afficheContrat, name="listeContrat"),
    path('rh/tables/contrat/fiche_journal/',views.fiche_journal_contrats, name="listeFiltrer"),
    path('rh/tables/contrat/<int:id>/', views.contrat_detail, name='contrat_detail'),
    path('employe/contratEMP/', views.contrat_detail_EMP, name='contrat_detail_EMP'),
    path('rh/tables/contrat/ajouter/',views.ajouterContrat, name="ajouterContrat"),
    path('rh/tables/contrat/edit/<int:pk>/',views.modifierContrat, name="modifierContrat"),
    path('rh/tables/contrat/supprimer/<int:pk>/',views.supprimerContrat, name="supprimerContrat"),
    path('rh/tables/contrat/archives/', views.archiveContrat, name="archiveContrat"),
    path('rh/tables/contrat/check_expiration/', views.check_contrat_expiration, name="checkContratExpiration") , 
    path('rh/tables/contrat/<int:contrat_id>/export/', views.export_contrat_csv, name='export_contrat_csv'),

]
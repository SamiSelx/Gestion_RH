from django.urls import path
from . import views

urlpatterns = [
    path('contrat/',views.afficheContrat, name="listeContrat"),
    path('contrat/fiche_journal/',views.fiche_journal_contrats, name="listeFiltrer"),
    path('contrat/<int:id>/', views.contrat_detail, name='contrat_detail'),
    path('contrat/ajouter/',views.ajouterContrat, name="ajouterContrat"),
    path('contrat/edit/<int:pk>/',views.modifierContrat, name="modifierContrat"),
    path('contrat/supprimer/<int:pk>/',views.supprimerContrat, name="supprimerContrat"),
    path('contrat/archives/', views.archiveContrat, name="archiveContrat"),
    path('contrat/check_expiration/', views.check_contrat_expiration, name="checkContratExpiration") , 
    path('contrat/<int:contrat_id>/export/', views.export_contrat_csv, name='export_contrat_csv'),

]
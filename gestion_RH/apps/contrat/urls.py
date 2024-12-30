from django.urls import path
from . import views

urlpatterns = [
    path('contrat/',views.afficheContrat, name="listeContrat"),
    path('contrat/ajouter/',views.ajouterContrat, name="ajouterContrat"),
    path("contrat/edit/<int:pk>",views.modifierContrat, name="modifierContrat"),
    path("contrat/supprimer/<int:pk>",views.supprimerContrat, name="supprimerContrat")
]
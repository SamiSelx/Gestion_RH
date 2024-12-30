from django.urls import path
from . import views

urlpatterns = [
    path('competence/',views.listeCompetence,name='listeCompetence'),
    path('competence/ajouter',views.ajouterCompetence,name='ajouterCompetence'),
    path('competence/modifier/<int:pk>',views.modifierCompetence,name='modifierCompetence'),
    path('competence/supprimer/<int:pk>',views.supprimerCompetence,name='supprimerCompetence'),
]
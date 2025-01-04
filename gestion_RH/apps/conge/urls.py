from django.urls import path
from . import views

urlpatterns = [
    path('tables/conge/', views.liste_conges, name='liste_conges'),
    path('tables/conge/creer/', views.creer_conge, name='creer_conge'),
    path('tables/conge/modifier/<int:id>/', views.modifier_conge, name='modifier_conge'),
    path('tables/conge/supprimer/<int:id>/', views.supprimer_conge, name='supprimer_conge'),
    path('conge/', views.listeCongeEmploye, name='listeCongeEmploye'),
    path('conge/approve/<int:id>', views.approveCongeEmploye, name='approveCongeEmploye'),
    path('conge/termine/<int:id>', views.termineCongeEmploye, name='termineCongeEmploye'),
    path('conge/supprimer/<int:id>', views.supprimerDemandeConge, name='supprimerDemandeConge'),
]

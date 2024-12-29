from django.urls import path
from . import views

urlpatterns = [
    path('objectif/',views.listeObjectif,name='listeObjectif'),
    path('objectif/ajouter',views.ajouterObjectif,name='ajouterObjectif'),
    path('objectif/modifier/<int:pk>',views.modifierObjectif,name='modifierObjectif'),
    path('objectif/supprimer/<int:pk>',views.supprimerObjectif,name='supprimerObjectif'),
]
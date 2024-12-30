from django.urls import path
from . import views

urlpatterns = [
    path('candidat/',views.listeCandidat,name='listeCandidat'),
    path('candidat/ajouter',views.ajouterCandidat,name='ajouterCandidat'),
    path('candidat/modifier/<int:pk>',views.modifierCandidat,name='modifierCandidat'),
    path('candidat/supprimer/<int:pk>',views.supprimerCandidat,name='supprimerCandidat'),
]
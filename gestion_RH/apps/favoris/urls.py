# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('rh/fonctionnalites/', views.listeFonctionnalites, name='listeFonctionnalites'),
    path('rh/fonctionnalites/ajouter/', views.ajouterFonctionnalite, name='ajouter_fonctionnalite'),
    path('rh/fonctionnalites/supprimer/<int:pk>/', views.supprimerFonctionnalite, name='supprimer_fonctionnalite'),
    path('rh/fonctionnalites/ajouter-favoris/<int:pk>/', views.ajouterAuxFavoris, name='ajouter_favoris'),
    path('rh/fonctionnalites/retirer-favoris/<int:pk>/', views.retirerDesFavoris, name='retirer_favoris'),
    path('rh/favoris/ajouter/', views.ajouter_to_favoris, name='ajouter_to_favoris'),
    path('rh/favoris/gerer/', views.gerer_favoris, name='gerer_favoris'),
    path('rh/favoris/gerer/edit/<int:favorisId>', views.edit_favoris, name='edit_favoris'),
    path('rh/favoris/gerer/supprimer/<int:favorisId>', views.supprimer_favoris, name='supprimer_favoris'),
    # path('fonctionnalites/favoris/', views.favoris_view, name='favoris_view'),
]


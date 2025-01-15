# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('fonctionnalites/', views.listeFonctionnalites, name='listeFonctionnalites'),
    path('fonctionnalites/ajouter/', views.ajouterFonctionnalite, name='ajouter_fonctionnalite'),
    path('fonctionnalites/supprimer/<int:pk>/', views.supprimerFonctionnalite, name='supprimer_fonctionnalite'),
    path('fonctionnalites/ajouter-favoris/<int:pk>/', views.ajouterAuxFavoris, name='ajouter_favoris'),
    path('fonctionnalites/retirer-favoris/<int:pk>/', views.retirerDesFavoris, name='retirer_favoris'),
    # path('fonctionnalites/favoris/', views.favoris_view, name='favoris_view'),
]


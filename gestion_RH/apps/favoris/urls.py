# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('fonctionnalites/', views.listeFonctionnalites, name='listeFonctionnalites'),
    path('fonctionnalites/ajouter/', views.ajouterFonctionnalite, name='ajouter_fonctionnalite'),
    path('fonctionnalites/supprimer/<int:pk>/', views.supprimerFonctionnalite, name='supprimer_fonctionnalite'),
    path('favoris/', views.listeFavoris, name='listeFavoris'),
    path('favoris/ajouter/<int:pk>/', views.ajouterAuxFavoris, name='ajouterAuxFavoris'),
    path('favoris/supprimer/<int:pk>/', views.supprimerDesFavoris, name='supprimerDesFavoris'),

]


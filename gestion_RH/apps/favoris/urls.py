# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('rh/favoris/ajouter/', views.ajouter_to_favoris, name='ajouter_to_favoris'),
    path('rh/favoris/gerer/', views.gerer_favoris, name='gerer_favoris'),
    path('rh/favoris/gerer/edit/<int:favorisId>', views.edit_favoris, name='edit_favoris'),
    path('rh/favoris/gerer/supprimer/<int:favorisId>', views.supprimer_favoris, name='supprimer_favoris'),
]


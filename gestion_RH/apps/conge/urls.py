from django.urls import path
from . import views

urlpatterns = [
    path('conge/', views.liste_conges, name='liste_conges'),
    path('conge/creer/', views.creer_conge, name='creer_conge'),
    path('conge/modifier/<int:id>/', views.modifier_conge, name='modifier_conge'),
    path('conge/supprimer/<int:id>/', views.supprimer_conge, name='supprimer_conge'),
]

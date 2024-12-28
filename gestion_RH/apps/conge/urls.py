from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_conges, name='liste_conges'),
    path('creer/', views.creer_conge, name='creer_conge'),
    path('modifier/<int:id>/', views.modifier_conge, name='modifier_conge'),
    path('supprimer/<int:id>/', views.supprimer_conge, name='supprimer_conge'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('rh/prime/', views.liste_primes, name='liste_primes'),
    path('rh/prime/creer/', views.creer_prime, name='creer_prime'),
    path('rh/prime/modifier/<int:id>/', views.modifier_prime, name='modifier_prime'),
    path('rh/prime/supprimer/<int:id>/', views.supprimer_prime, name='supprimer_prime'),
]

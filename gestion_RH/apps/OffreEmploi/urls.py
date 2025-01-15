# apps/Formation/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('rh/tables/offreEmploye/create/', views.create_offre_employe, name='create_offre_employe'),
    path('rh/tables/offreEmploye/', views.liste_offre_employe, name='liste_offre_employe'),
    path('rh/tables/offreEmploye/update/<int:pk>/', views.update_offre_employe, name='update_offre_employe'),
    path('rh/tables/offreEmploye/delete/<int:pk>/', views.delete_offre_employe, name='delete_offre_employe'),
    path('offreEmploye/<int:id>/', views.offreEmploye_detail, name='offreEmploye_detail'),
]

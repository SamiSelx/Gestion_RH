# apps/Formation/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('offreEmploye/create/', views.create_offre_employe, name='create_offre_employe'),
    path('offreEmploye/', views.liste_offre_employe, name='liste_offre_employe'),
    path('offreEmploye/update/<int:pk>/', views.update_offre_employe, name='update_offre_employe'),
    path('offreEmploye/delete/<int:pk>/', views.delete_offre_employe, name='delete_offre_employe'),
    path('offreEmploye/<int:id>/', views.offreEmploye_detail, name='offreEmploye_detail'),

]

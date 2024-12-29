# apps/Formation/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_offre_employe, name='create_offre_employe'),
    path('list/', views.liste_offre_employe, name='liste_offre_employe'),
    path('update/<int:pk>/', views.update_offre_employe, name='update_offre_employe'),
    path('delete/<int:pk>/', views.delete_offre_employe, name='delete_offre_employe'),
]

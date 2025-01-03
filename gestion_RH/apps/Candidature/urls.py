# apps/Formation/urls.py

from django.urls import path
from . import views

urlpatterns = [
path('candidatures/offres/<int:offre_id>/postuler/', views.postuler_offre, name='postuler_offre'),
path('candidatures/<int:candidature_id>/entretien/', views.planifier_entretien, name='planifier_entretien'),
path('candidatures/', views.liste_candidatures, name='liste_candidatures'),
path('candidatures/modifier_statut/<int:candidature_id>/', views.modifier_statut, name='modifier_statut'),
path('candidatures/details/<int:id>/', views.candidature_detail, name='detail_candidature'),


]

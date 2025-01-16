# apps/Formation/urls.py

from django.urls import path
from . import views

urlpatterns = [
path('candidatures/offres/<int:offre_id>/postuler/', views.postuler_offre, name='postuler_offre'),
path('rh/tables/candidatures/<int:candidature_id>/entretien/', views.planifier_entretien, name='planifier_entretien'),
path('rh/tables/candidatures/', views.liste_candidatures, name='liste_candidatures'),
path('rh/tables/candidatures/modifier_statut/<int:candidature_id>/', views.modifier_statut, name='modifier_statut'),
path('rh/tables/candidatures/details/<int:id>/', views.candidature_detail, name='detail_candidat'),
path('rh/AnalyseRecrutements/', views.analyse_recrutement, name='analyse_recrutement'),
path('success/', views.success_page, name='successPage'),

]

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
path('rh/planification/', views.planification_entretien_list, name='planification_entretien_list'),
path('rh/planification/modifier/<int:entretien_id>/', views.modifier_entretien, name='modifier_entretien'),
path('rh/planification/supprimer/<int:entretien_id>/', views.supprimer_entretien, name='supprimer_entretien'),
path('success/', views.success_page, name='successPage'),

]

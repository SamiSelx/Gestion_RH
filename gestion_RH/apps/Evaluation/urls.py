from django.urls import path
from . import views

urlpatterns = [
    path('manager/evaluations/', views.list_evaluations, name='list_evaluations'),
    path('rh/evaluations_consultation/', views.list_evaluations_consultation, name='list_evaluations_consultation'),
    path('rh/evaluations/report/<int:pk>/', views.consultation_report_RH, name='consultation_report'),
    path('rh/evaluations/top-employees/', views.top_employees_consultation, name='top_employees_consultation'),

    path('manager/evaluations/create/', views.create_evaluation, name='create_evaluation'),
    path('manager/evaluations/update/<int:pk>/', views.update_evaluation, name='update_evaluation'),
    path('manager/evaluations/delete/<int:pk>/', views.delete_evaluation, name='delete_evaluation'),
    path('manager/evaluations/add-criteria/<int:pk>/', views.add_criteria_scores, name='add_criteria_scores'),
    path('manager/evaluations/report/<int:pk>/', views.generate_report, name='generate_report'),
    path('manager/evaluations/top-employees/', views.top_employees, name='top_employees'),
    path('manager/modal-criteria/<int:evaluation_id>/', views.modal_criteria_view, name='modal_criteria'),
    path('manager/faire_evaluation/<int:evaluation_id>/', views.faire_evaluation, name='faire_evaluation'),
    #-------------------------------------------------------------------
    path('manager/objectifs/<int:employe_id>/<int:evaluation_id>/', views.objectifs_pour_evaluation, name='objectifs_pour_evaluation'),
    path('manager/objectifs/attient/<int:evaluation_id>/<int:objectif_id>/', views.marquer_objectif_attient, name='marquer_objectif_attient'),
    #-------------------------------------------------------------------
    path('manager/criteres/', views.list_criteres, name='list_criteres'),
    path('manager/criteres/create/', views.create_critere, name='create_critere'),
    path('manager/criteres/update/<int:pk>/', views.update_critere, name='update_critere'),
    path('manager/criteres/delete/<int:pk>/', views.delete_critere, name='delete_critere'),
]

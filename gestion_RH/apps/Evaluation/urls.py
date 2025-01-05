from django.urls import path
from . import views

urlpatterns = [
    path('evaluations/', views.list_evaluations, name='list_evaluations'),
    path('evaluations/create/', views.create_evaluation, name='create_evaluation'),
    path('evaluations/update/<int:pk>/', views.update_evaluation, name='update_evaluation'),
    path('evaluations/delete/<int:pk>/', views.delete_evaluation, name='delete_evaluation'),
    path('evaluations/add-criteria/<int:pk>/', views.add_criteria_scores, name='add_criteria_scores'),
    path('evaluations/report/<int:pk>/', views.generate_report, name='generate_report'),
    path('evaluations/top-employees/', views.top_employees, name='top_employees'),
    #-------------------------------------------------------------------
    path('criteres/', views.list_criteres, name='list_criteres'),
    path('criteres/create/', views.create_critere, name='create_critere'),
    path('criteres/update/<int:pk>/', views.update_critere, name='update_critere'),
    path('criteres/delete/<int:pk>/', views.delete_critere, name='delete_critere'),
]

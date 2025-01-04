from django.contrib import admin
from django.urls import path
from . import views
from ..conge.views import demandeConge
from django.shortcuts import render

urlpatterns = [
    path('',views.home,name='home'),
    path('rh/tables/',views.RhTables,name='tables'),
    path('rh/',views.RhRedirect),
    path('rh/analyse/employe',views.employeeAnalyses,name='employeeAnalyses'),
    path('employe/',views.employe,name='employePage'),
    path('employe/demandeConge',demandeConge,name='demandeConge'),
    path('employe/information',views.informationPersonnel,name='informationPersonnel')
]

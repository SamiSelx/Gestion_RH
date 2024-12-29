from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('rh/tables/',views.RhTables,name='tables'),
    path('rh/',views.RhRedirect)
]

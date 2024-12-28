from django.urls import path
from . import views

urlpatterns = [
    path('', views.employe_list, name='employe_list'),
    path('<int:code_employe>/', views.employe_detail, name='employe_detail'),
    path('create/', views.employe_create, name='employe_create'),
    path('<int:code_employe>/update/', views.employe_update, name='employe_update'),
    path('<int:code_employe>/delete/', views.employe_delete, name='employe_delete'),
]

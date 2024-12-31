from django.urls import path
from . import views

urlpatterns = [
    path('employe/', views.employe_list, name='employe_list'),
    path('employe/<int:id>/', views.employe_detail, name='employe_detail'),
    path('employe/create/', views.employe_create, name='employe_create'),
    path('employe/<int:id>/update/', views.employe_update, name='employe_update'),
    path('employe/<int:id>/delete/', views.employe_delete, name='employe_delete'),
    path('employe/<int:employe_id>/export/', views.export_employe_csv, name='export_employe_csv'),
]

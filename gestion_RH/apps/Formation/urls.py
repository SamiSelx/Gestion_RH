from django.urls import path
from . import views

urlpatterns = [
    path('formation/', views.formation_list, name='ListeFormation'),
    path('formation/create/', views.create_formation, name='add_f'),
    path('formation/update/<int:pk>/', views.formation_update, name='update_f'),
    path('formation/delete/<int:pk>/', views.formation_delete, name='delete_f'),
]

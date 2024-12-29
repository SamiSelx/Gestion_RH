from django.urls import path
from . import views

urlpatterns = [
    path('', views.formation_list, name='ListeFormation'),
    path('create/', views.create_formation, name='add_f'),
    path('update/<int:pk>/', views.formation_update, name='update_f'),
    path('delete/<int:pk>/', views.formation_delete, name='delete_f'),
]

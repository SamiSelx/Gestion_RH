from django.urls import path
from . import views

urlpatterns = [
    path('service/', views.service_list, name='service_list'),
    path('service/add/', views.add_service, name='add_service'),
    path('service/edit/<int:pk>/', views.edit_service, name='edit_service'),
    path('service/delete/<int:pk>/', views.delete_service, name='delete_service'),
]

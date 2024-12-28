from django.contrib import admin
from .models import Employe,Contrat,Service,Conge

# Register your models here.
admin.site.register(Service)
admin.site.register(Employe)
admin.site.register(Contrat)
admin.site.register(Conge)
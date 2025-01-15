from django.contrib import admin
from .models import Employe,Contrat,Service,Conge,DemandeConge,Competence,Formation,Objectif,Salaire,Prime,Absence,Candidat

# Register your models here.
admin.site.register(Service)
admin.site.register(Employe)
admin.site.register(Contrat)
admin.site.register(Conge)
admin.site.register(DemandeConge)
admin.site.register(Competence)
admin.site.register(Formation)
admin.site.register(Objectif)
admin.site.register(Salaire)
admin.site.register(Absence)
admin.site.register(Prime)
admin.site.register(Candidat)

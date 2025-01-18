from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Service)
admin.site.register(models.Employe)
admin.site.register(models.Contrat)
admin.site.register(models.Conge)
admin.site.register(models.DemandeConge)
admin.site.register(models.Competence)
admin.site.register(models.Formation)
admin.site.register(models.Objectif)
admin.site.register(models.Salaire)
admin.site.register(models.Absence)
admin.site.register(models.Prime)
admin.site.register(models.Candidat)
admin.site.register(models.Candidature)
admin.site.register(models.Offre_employe)
admin.site.register(models.FicheDePaieS)


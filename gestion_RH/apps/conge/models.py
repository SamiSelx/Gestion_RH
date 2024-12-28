from django.db import models

class Conge(models.Model):
    code = models.CharField(max_length=50)
    employe = models.CharField(max_length=100)    
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_conge = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.employe}"

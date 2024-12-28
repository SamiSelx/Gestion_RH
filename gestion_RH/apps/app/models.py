from django.db import models

class Service(models.Model):
    description_service = models.TextField()

    def __str__(self):
        return self.description_service

class Employe(models.Model):
    nomE = models.CharField(max_length=100)
    prenomE = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_naissance_E = models.DateField()
    date_embauche_E = models.DateField()
    adresse_E = models.TextField()
    code_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='employes')

    def __str__(self):
        return f"{self.nomE} {self.prenomE}"


class Contrat(models.Model):
    type_contrat = models.CharField(max_length=100)
    date_debut_contrat = models.DateField()
    date_fin_contrat = models.DateField()
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    etat = models.CharField(max_length=50)
    code_employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='contrats')

class Conge(models.Model):
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_conge = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    code_employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='conges')  

    def __str__(self):
        return f"{self.id} - {self.code_employe}"

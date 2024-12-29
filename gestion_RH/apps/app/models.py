from django.db import models


# Section 1 :les Tables de la section  Favoris
class Employe(models.Model):
    code_employe = models.AutoField(primary_key=True)
    nomE = models.CharField(max_length=50)
    prenomE = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    date_naissance_E = models.DateField()
    date_embauche_E = models.DateField()
    adresse_E = models.CharField(max_length=100)
    code_service = models.ForeignKey('Service', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nomE} {self.prenomE}"

class Fonctionnalite(models.Model):
    code_fonctionnalite = models.AutoField(primary_key=True)
    path_fonctionnalite = models.CharField(max_length=100)

    def __str__(self):
        return self.path_fonctionnalite

class Favoris(models.Model):
    code_employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    code_fonctionnalite = models.ForeignKey(Fonctionnalite, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('code_employe', 'code_fonctionnalite')

    def __str__(self):
        return f"Favoris for {self.code_employe}: {self.code_fonctionnalite}"

class Service(models.Model):
    code_service = models.AutoField(primary_key=True)
    description_service = models.CharField(max_length=100)

    def __str__(self):
        return self.description_service

class Formation(models.Model):
    titre_formation = models.CharField(max_length=100)
    description_formation = models.TextField()

    def __str__(self):
        return self.titre_formation



class Offre_employe(models.Model):
  
    titre_offre = models.CharField(max_length=100)
    code_service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='offres')

    def __str__(self):
        return self.titre_offre
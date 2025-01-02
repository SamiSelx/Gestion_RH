from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    description_service = models.CharField(max_length=100)

    def __str__(self):
        return self.description_service

class Competence(models.Model):
    nom_competence = models.CharField(max_length=255)
    description_competence = models.TextField()

    def __str__(self):
        return self.nom_competence

class Formation(models.Model):
    titre_formation = models.CharField(max_length=100)
    description_formation = models.TextField()

    def __str__(self):
        return self.titre_formation
    
class Employe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employes', null=True, blank=True)
    nomE = models.CharField(max_length=50)
    prenomE = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    date_naissance_E = models.DateField()
    date_embauche_E = models.DateField()
    adresse_E = models.CharField(max_length=100)
    code_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='employes')
    competences = models.ManyToManyField('Competence', related_name='employes')
    formations = models.ManyToManyField('Formation', related_name='employes')
    def __str__(self):
        return f"{self.nomE} {self.prenomE}"


class Contrat(models.Model):
    type_contrat = models.CharField(max_length=100,choices=[('CDI', 'Contrats à durée indéterminée'), ('CDD', ' contrats à durée déterminée'),('Stage','stage')])
    date_debut_contrat = models.DateField()
    date_fin_contrat = models.DateField()
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    etat = models.CharField(max_length=50)
    archive = models.BooleanField(default=False)
    code_employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='contrats')

class Conge(models.Model):
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_conge = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    code_employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='conges')  

    def __str__(self):
        return f"{self.id} - {self.code_employe}"
    
class Fonctionnalite(models.Model):
    name_Fonctionnalite = models.CharField(max_length=50)
    path_fonctionnalite = models.CharField(max_length=100)
    favoris = models.BooleanField(default=False)

    def __str__(self):
        return self.name_Fonctionnalite

# class Favoris(models.Model):
#     code_employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
#     code_fonctionnalite = models.ForeignKey(Fonctionnalite, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('code_employe', 'code_fonctionnalite')

#     def __str__(self):
#         return f"Favoris for {self.code_employe}: {self.code_fonctionnalite}"

class Offre_employe(models.Model):
  
    titre_offre = models.CharField(max_length=100)
    code_service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='offres')

    def __str__(self):
        return self.titre_offre


    
class Candidat(models.Model):
    nomC = models.CharField(max_length=100)
    prenomC = models.CharField(max_length=100)
    adresseC = models.TextField()
    tlfn_candidat = models.CharField(max_length=20)

class Objectif(models.Model):
    description_objectif = models.TextField()
    date_limite = models.DateField()
    code_employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='objectifs')
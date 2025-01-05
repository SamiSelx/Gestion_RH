from django.db import models
from django.contrib.auth.models import User


from datetime import date
# from ..authentification.models import CustomUser
    
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

class Competence(models.Model):
    nom_competence = models.CharField(max_length=50)
    description_competence = models.TextField()

    def __str__(self):
        return f"Competence {self.nom_competence}"
       
class Employe(models.Model):
    ROLE_CHOICES = [
        ('RH', 'RH'),
        ('Manager', 'Manager'),
        ('Employe', 'Employe'),
    ]
    nomE = models.CharField(max_length=50)
    prenomE = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    date_naissance_E = models.DateField()
    date_embauche_E = models.DateField()
    adresse_E = models.CharField(max_length=100)
    solde_annuel = models.IntegerField(default=30) # par default 30 jours par année
    code_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='employes')
    competences = models.ManyToManyField('Competence', related_name='employes')
    formations = models.ManyToManyField('Formation', related_name='employes')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Employe')
    

    def __str__(self):
        return f"{self.nomE} {self.prenomE}"


class Contrat(models.Model):
    TYPES_CONTRAT = [
        ('CDI', 'Contrat à Durée Indéterminée'),
        ('CDD', 'Contrat à Durée Déterminée'),
        ('Stagiaire', 'Internship'),
    ]
    type_contrat = models.CharField(max_length=20,choices=TYPES_CONTRAT)
    date_debut_contrat = models.DateField()
    date_fin_contrat = models.DateField()
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    etat = models.CharField(max_length=50)
    archive = models.BooleanField(default=False)
    code_employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='contrats')

class Conge(models.Model):
    TYPE_CONGE_CHOICES = [
        ('Annuel', 'Congé annuel'),
        ('Maladie', 'Congé maladie'),
        ('Maternité', 'Congé maternité'),
        ('Paternité', 'Congé paternité'),
        ('Sans solde', 'Congé sans solde'),
        ('Exceptionnel', 'Congé exceptionnel'),
    ]
    type_conge = models.CharField(max_length=20,choices=TYPE_CONGE_CHOICES,default='Annuel')
    # code_employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='conges')  

    def __str__(self):
        return f"{self.type_conge}"
    
class DateConge(models.Model):
    date_debut = models.DateField(unique=True)

# solde_annuel = jours disponibles | en peut avoir le jour demandé en utilisant date debut et fin
class DemandeConge(models.Model):
    code_employe = models.ForeignKey(Employe,on_delete=models.CASCADE, related_name='demandeConges')
    code_conge = models.ForeignKey(Conge, on_delete=models.CASCADE, related_name='demandeConges')
    # date_debut = models.ForeignKey(DateConge, on_delete=models.CASCADE, related_name='demandeConges')
    date_debut = models.DateField() # for testing then i'll do with foreignKey
    date_fin = models.DateField()
    jours_demandes = models.IntegerField(null=True)
    # add description
    # description = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=[('En attente', 'En attente'), ('Approuvé', 'Approuvé'), ('Rejeté', 'Rejeté'), ('Terminé', 'Terminé')],
        default='En attente'
    )


    def calculer_jours_demandes(self):
        self.jours_demandes =  (self.date_fin - self.date_debut).days + 1
        return self.jours_demandes
    def changeStatus(self,status):
        self.status = status
        self.save()
    # reduire le solde de l'employe (on consider que l'employe utilise tous les jours demandé)
    def mettre_a_jour_solde(self):
        jours_demandes = self.calculer_jours_demandes()
        if self.code_employe.solde_annuel < jours_demandes and self.code_conge.type_conge == "Annuel":
            raise ValueError("L'employé n'a pas de solde")
        if self.status == 'Approuvé' and self.code_conge.type_conge == "Annuel":
            # Réduire le solde annuel de l'employé en fonction des jours demandés
            self.code_employe.solde_annuel -= jours_demandes
            self.code_employe.save()

    def calculer_jours_reellement_utilises(self):
        if self.status == 'Terminé':
            raise ValueError("Le congé est déjà terminé.")
        # Calcul des jours entre la date de début et la date actuelle
        if (date.today() - self.date_debut).days + 1 >= 0:
            jours_utilises = (date.today() - self.date_debut).days + 1  # Inclut le jour de début
        else: jours_utilises = 0
        return max(0, min(jours_utilises, self.jours_demandes))

    # si on click sur (change status) a terminé
    def cloturer_conge(self):
        if self.status != "Terminé":
            # self.jours_utilises = jours_reellement_utilises
            jours_utilises = self.calculer_jours_reellement_utilises()
            # Remettre les jours non utilisés dans le solde annuel de l'employé
            if self.code_conge.type_conge == 'Annuel':
                self.code_employe.solde_annuel += (self.calculer_jours_demandes() - jours_utilises)
            self.status = 'Terminé'
            self.code_employe.save()
            self.save()
    
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
    description = models.TextField()
    location = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    code_service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='offres')

    def __str__(self):
        return self.titre_offre


    
class Candidat(models.Model):
    nomC = models.CharField(max_length=100)
    prenomC = models.CharField(max_length=100)
    adresseC = models.TextField()
    tlfn_candidat = models.CharField(max_length=20)
    def __str__(self):
        return self.nomC

class Candidature(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='candidatures')
    offre = models.ForeignKey(Offre_employe, on_delete=models.CASCADE, related_name='candidatures')
    date_soumission = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=50,
        choices=[
            ('Reçue', 'Reçue'),
            ('En cours de traitement', 'En cours de traitement'),
            ('Rejetée', 'Rejetée'),
            ('Acceptée', 'Acceptée'),
        ],
        default='Reçue'
    )
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    
    def __str__(self):
        return f"Candidature {self.candidat.nomC} - {self.offre.titre_offre}"

class Entretien(models.Model):
    candidature = models.ForeignKey(Candidature, on_delete=models.CASCADE, related_name='entretiens')
    date_entretien = models.DateTimeField()
    lieu = models.CharField(max_length=200)
    commentaires = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Entretien pour {self.candidature.candidat.nomC} - {self.date_entretien}"


class Objectif(models.Model):
    description_objectif = models.TextField()
    date_limite = models.DateField()
    code_employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='objectifs')

# ------------------------Evaluation -----------------------------
class Evaluation(models.Model):
    date_evaluation = models.DateField()
    note_evaluation_totale = models.FloatField(default=0.0)
    type_evaluation = models.CharField(
        max_length=20,
        choices=[('Annual', 'Annual'), ('Semi-Annual', 'Semi-Annual')],
        default='Annual'
    )
    employe_manager = models.ForeignKey(
        'Employe', on_delete=models.CASCADE, related_name='evaluations_as_manager'
    )
    employe = models.ForeignKey(
        'Employe', on_delete=models.CASCADE, related_name='evaluations_as_employee'
    )

class CriterEvaluation(models.Model):
    description_critere = models.CharField(max_length=255)
    def __str__(self):
        return self.description_critere
    
class EvaluerCritere(models.Model):
    code_critere = models.ForeignKey(CriterEvaluation, on_delete=models.CASCADE)
    code_evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    note_critere_evaluer = models.FloatField()

class RapportEvaluation(models.Model):
    date_rapport = models.DateField()
    contenu_rapport = models.TextField()
    code_evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='rapports')

    def __str__(self):
        return f"Rapport for Evaluation {self.code_evaluation}"


class RapportPartage(models.Model):
    code_rapport = models.ForeignKey(RapportEvaluation, on_delete=models.CASCADE, related_name='shared_with')
    code_employe = models.ForeignKey('Employe', on_delete=models.CASCADE, related_name='shared_reports')

    def __str__(self):
        return f"Rapport {self.code_rapport} shared with {self.code_employe}"

#-----------------Objectif----------------------
class Objectif(models.Model):
    description_objectif = models.TextField()
    date_limite = models.DateField()
    code_employe = models.ForeignKey('Employe', on_delete=models.CASCADE, related_name='objectifs')

    def __str__(self):
        return f"Objectif for {self.code_employe}"

class ObjectifAttient(models.Model):
    code_evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='objectifs_attient')
    code_objectif = models.ForeignKey(Objectif, on_delete=models.CASCADE, related_name='objectifs_attient')
    attient = models.BooleanField(default=False)

    def __str__(self):
        return f"Objective {self.code_objectif} achieved: {self.attient}"


#------------- Competence --------------------------

    
class DeveloperCompetence(models.Model):
    code_evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='competences_developped')
    code_competence = models.ForeignKey('Competence', on_delete=models.CASCADE)
    niveau_CE = models.IntegerField()

    def __str__(self):
        return f"Competence {self.code_competence} in Evaluation {self.code_evaluation}"



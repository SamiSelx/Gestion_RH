from django.contrib.auth.models import AbstractUser
from django.db import models
from ..app.models import Employe

class CustomUser(AbstractUser):
    # ROLE_CHOICES = [
    #     ('RH', 'RH'),
    #     ('Manager', 'Manager'),
    #     ('Employee', 'Employee'),
    #     ('Candidat', 'Candidat'),
    # ]
    # role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Candidat')
    # when u assign employe add role
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.username
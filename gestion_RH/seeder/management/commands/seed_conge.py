from django.core.management.base import BaseCommand
from apps.app.models import Conge 

class Command(BaseCommand):
    help = "Seed the Conge model with predefined leave types."

    def handle(self, *args, **kwargs):
        conge_types_choice = [
         'Congé annuel',
         'Congé maladie',
         'Congé maternité',
         'Congé paternité',
        'Congé sans solde',
        'Congé exceptionnel',
    ]

        for type in conge_types_choice:
            Conge.objects.get_or_create(conge_types=type.split()[1])

        self.stdout.write(self.style.SUCCESS("Successfully seeded Conge model!"))

from apps.app.models import Fonctionnalite
from django.shortcuts import render

def favoris_context(request):
    favoris_list = Fonctionnalite.objects.filter(favoris=True)
    return {'favoris_list': favoris_list}
from apps.app.models import Fonctionnalite,Favoris
from django.shortcuts import render

def favoris_context(request):
    # favoris_list = Fonctionnalite.objects.filter(favoris=True)
    if request.user.is_authenticated:
        favoris_list = Favoris.objects.filter(user=request.user)
        return {'favoris_list': favoris_list}
    return {}
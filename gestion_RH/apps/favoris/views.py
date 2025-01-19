from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.app.models import Favoris
from django.contrib.auth.decorators import login_required


def ajouter_to_favoris(request):
    if request.method == 'POST':
        path = request.POST.get('fonctionnalite')
        path = path.rstrip('/')
        name = request.POST.get('nameFonctionnalite')  
        if path and name:
            Favoris.objects.get_or_create(user=request.user, path=path, defaults={'name': name})

    # return same page
    return redirect(request.META.get('HTTP_REFERER', '/') ) 

def gerer_favoris(request):
    favoris = Favoris.objects.filter(user=request.user)
    return render(request,'pages/rh/favoris/listeFavoris.html',{'favoris':favoris})

def edit_favoris(request,favorisId):
    favoris = Favoris.objects.get(id=favorisId,user=request.user)
    if request.method == 'POST':
        name = request.POST.get('nameFavoris')
        if name:
            favoris.name = name
            favoris.save()
            return redirect('gerer_favoris')
        messages.add_message(request,messages.ERROR,'you must write a new name')
        
    return render(request,'pages/rh/favoris/editFavoris.html',{'favoris':favoris})

def supprimer_favoris(request,favorisId):
    favoris = Favoris.objects.get(id=favorisId,user=request.user)
    if request.method == 'POST':
        favoris.delete()
    return redirect('gerer_favoris')



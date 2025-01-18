from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.app.models import Fonctionnalite,Favoris
from .forms import FonctionnaliteForm
from django.contrib.auth.decorators import login_required

# CRUD for Fonctionnalites
def listeFonctionnalites(request):
    fonctionnalites = Fonctionnalite.objects.all()
    return render(request, 'pages/fonctionnalite/listeFonctionnalites.html', {'fonctionnalites': fonctionnalites})

def ajouterFonctionnalite(request):
    if request.method == 'POST':
        print(request.POST.get("fonctionnalite"))
        form = FonctionnaliteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeFonctionnalites')
    else:
        form = FonctionnaliteForm()
    return render(request, 'pages/fonctionnalite/ajouter_fonctionnalite.html', {'form': form})

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

def supprimerFonctionnalite(request, pk):
    fonctionnalite = get_object_or_404(Fonctionnalite, id=pk)
    if request.method == 'POST':
        fonctionnalite.delete()
        return redirect('listeFonctionnalites')
    return render(request, 'pages/fonctionnalite/supprimer_fonctionnalite.html', {'fonctionnalite': fonctionnalite})

def ajouterAuxFavoris(request, pk):
    fonctionnalite = get_object_or_404(Fonctionnalite, id=pk)
    fonctionnalite.favoris = True
    fonctionnalite.save()
    messages.success(request, "La fonctionnalité a été ajouté  aux favoris.")
    return redirect('listeFonctionnalites')  

def retirerDesFavoris(request, pk):
    fonctionnalite = get_object_or_404(Fonctionnalite, id=pk)
    fonctionnalite.favoris = False
    fonctionnalite.save()
    messages.success(request, "La fonctionnalité a été retirer aux favoris.")
    return redirect('listeFonctionnalites')  

# def favoris_view(request):
#     favoris_list = Fonctionnalite.objects.filter(favoris=True)  
#     return render(request, 'base.html', {'favoris_list': favoris_list})


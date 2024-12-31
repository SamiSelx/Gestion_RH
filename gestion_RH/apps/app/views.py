from django.shortcuts import render,redirect
from .models import Offre_employe
# from django.contrib.auth.decorators import login_required

# @login_required
def home(request):
    offres = Offre_employe.objects.all()
    return render(request,"pages/home/index.html",{'offres': offres})

def RhTables(request):
    return render(request,"pages/RH/tables/tables.html")

def RhRedirect(request):
    return redirect('tables')
    
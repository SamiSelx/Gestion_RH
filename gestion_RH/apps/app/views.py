from django.shortcuts import render,redirect
# from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
def home(request):
    return render(request,"pages/home/index.html")

def RhTables(request):
    return render(request,"pages/RH/tables/tables.html")

def RhRedirect(request):
    return redirect('tables')
    
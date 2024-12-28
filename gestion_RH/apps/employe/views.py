from django.shortcuts import render, get_object_or_404, redirect
from apps.app.models import Employe  
from .forms import EmployeForm  




#---------------------CRUD Employe-------------------------------



def employe_list(request):
    employes = Employe.objects.all()
    return render(request, 'pages/Employe/employe_list.html', {'employes': employes})


def employe_detail(request, code_employe):
    employe = get_object_or_404(Employe, code_employe=code_employe)
    return render(request, 'pages/Employe/employe_detail.html', {'employe': employe})


def employe_create(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employe_list')
    else:
        form = EmployeForm()
    return render(request, 'pages/Employe/employe_form.html', {'form': form})

def employe_update(request, code_employe):
    employe = get_object_or_404(Employe, code_employe=code_employe)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('employe_list')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'pages/Employe/employe_form.html', {'form': form})


def employe_delete(request, code_employe):
    employe = get_object_or_404(Employe, code_employe=code_employe)
    if request.method == 'POST':
        employe.delete()
        return redirect('employe_list')
    return render(request, 'pages/Employe/employe_confirm_delete.html', {'employe': employe})
#-----------------------------------------------------------------


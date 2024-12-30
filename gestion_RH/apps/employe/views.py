from django.shortcuts import render, get_object_or_404, redirect
from apps.app.models import Employe
from django.core.paginator import Paginator
from .forms import EmployeForm

def employe_list(request):
    employes_list = Employe.objects.all()
    paginator = Paginator(employes_list, 10)

    page_number = request.GET.get('page')
    employes = paginator.get_page(page_number)
    return render(request, 'pages/rh/tables/Employe/employe_list.html', {'employes': employes})


def employe_detail(request, id):  # Changed code_employe to id
    employe = get_object_or_404(Employe, id=id)  # Changed code_employe to id
    return render(request, 'pages/rh/tables/Employe/employe_detail.html', {'employe': employe})


def employe_create(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employe_list')
    else:
        form = EmployeForm()
    return render(request, 'pages/rh/tables/Employe/employe_form.html', {'form': form})


def employe_update(request, id):  # Changed code_employe to id
    employe = get_object_or_404(Employe, id=id)  # Changed code_employe to id
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('employe_list')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'pages/rh/tables/Employe/employe_form.html', {'form': form})


def employe_delete(request, id):  # Changed code_employe to id
    employe = get_object_or_404(Employe, id=id)  # Changed code_employe to id
    if request.method == 'POST':
        employe.delete()
        return redirect('employe_list')
    return render(request, 'pages/rh/tables/Employe/employe_confirm_delete.html', {'employe': employe})


from django.shortcuts import render, get_object_or_404, redirect
from apps.app.models import Service
from .forms import ServiceForm

# CREATE: Add a new service
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')  
    else:
        form = ServiceForm()
    return render(request, 'pages/service/add_service.html', {'form': form})

# READ: List all services
def service_list(request):
    services = Service.objects.all()
    return render(request, 'pages/service/service_list.html', {'services': services})

# UPDATE: Edit a service
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')  
    else:
        form = ServiceForm(instance=service)
    return render(request, 'pages/service/edit_service.html', {'form': form})

# DELETE: Delete a service
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')  
    return render(request, 'pages/service/delete_service.html', {'service': service})

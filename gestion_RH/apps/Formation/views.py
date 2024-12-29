from django.shortcuts import render, get_object_or_404, redirect
from apps.app.models import Formation
from .forms  import FormationForm


def create_formation(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ListeFormation')  
    else:
        form = FormationForm()
    return render(request, 'pages/Formation/add_f.html', {'form': form})


def formation_list(request):
    formations = Formation.objects.all()
    return render(request, 'pages/Formation/ListeFormation.html', {'formations': formations})




def formation_update(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            return redirect('ListeFormation')  
    else:
        form = FormationForm(instance=formation)
    return render(request, 'pages/Formation/update_f.html', {'form': form})

# Delete a Formation
def formation_delete(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        formation.delete()
        return redirect('ListeFormation')  
    return render(request, 'pages/Formation/delete_f.html', {'formation': formation})

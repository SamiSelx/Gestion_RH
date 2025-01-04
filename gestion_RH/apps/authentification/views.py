from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from ..app.models import Candidat

# Registration View
def register(request):
    if request.user.is_authenticated:
        return redirect('home') 
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # after register create candidat in the db
            # candidat = Candidat.objects.create(request.POST)
            messages.success(request, 'Registration successful.')
            return redirect("home")  
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
            print(form.errors)
    else:
        form = CreateUserForm()
    return render(request, 'registration/register.html', {'form': form})

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user)
          messages.success(request, 'Login successful.')
          return redirect("home") 
        else:
          messages.error(request, 'Invalid username or password.')
          return render(request, 'registration/login.html')

    else:
          return render(request, 'registration/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('home')



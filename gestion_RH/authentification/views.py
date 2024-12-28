from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm

# Registration View
def register(request):
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('Home/index.html')  
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
            print(form.errors)
    else:
        form = CreateUserForm()
    return render(request, 'auth/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user)
          messages.success(request, 'Login successful.')
          return redirect('Home/index.html') 
        else:
          messages.error(request, 'Invalid username or password.')
          return render(request, 'auth/login.html')

    else:
          return render(request, 'auth/login.html')





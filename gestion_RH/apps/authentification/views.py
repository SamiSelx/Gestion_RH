from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from ..app.models import Candidat
from .models import CustomUser
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings

def send_activation_mail(user,request):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = generate_token.make_token(user)
    body = render_to_string('registration/activate.html',{
        'user':user,
        'domain':current_site,
        'uid':uid,
        'token':token 
    })

    email = EmailMessage(subject=subject,body=body,from_email=settings.EMAIL_FROM_USER,to=[user.email])
    email.send()


def activate_user(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk= uid)

    except Exception as e:
        user = None
    
    if user and generate_token.check_token(user,token):
        user.isActive = True
        user.save()
        messages.add_message(request,messages.SUCCESS,'Email Verified, please try to login')
        return redirect('login')
    
    return render(request,'registration/activate_failed.html',{'user':user})

# Registration View
def register(request):
    if request.user.is_authenticated:
        return redirect('home') 
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # after register create candidat in the db
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            phone = request.POST.get('phone')
            adresse = request.POST.get('adresse')
            candidat = Candidat.objects.create(nomC=nom,prenomC=prenom,tlfn_candidat=phone,adresseC=adresse,user=user)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_activation_mail(user,request)
            messages.add_message(request,messages.SUCCESS,'Email is sent, please check your email to verify your Account')
            return redirect('login')
        else:
            messages.add_message(request,messages.ERROR, 'Registration failed. Please correct the errors below.')
    else:
        form = CreateUserForm()
    return render(request, 'registration/register.html', {'form': form})

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None and not user.isActive:
            messages.add_message(request,messages.ERROR,'Email is not verified, please Check your email!!')
            return render(request,'registration/login.html')
        if user is not None:
          login(request, user)
          messages.add_message(request,messages.SUCCESS, 'Login successful.')
          if not (user.employe is None):
              if user.employe.role == "Manager":
                  return redirect("managerPage")
              elif user.employe.role == "RH":
                  return redirect("dashboard")
              else: return redirect("employePage")

          return redirect("home") 
        else:
          messages.add_message(request,messages.ERROR, 'Invalid email or password.')
          return render(request, 'registration/login.html')

    else:
          return render(request, 'registration/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('home')



from django.shortcuts import render



# @login_required
def home(request):
    return render(request,"pages/home/index.html")






















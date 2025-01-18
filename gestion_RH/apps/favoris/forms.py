from django import forms
from apps.app.models import Fonctionnalite,Favoris

class FonctionnaliteForm(forms.ModelForm):
    class Meta:
        model = Fonctionnalite
        fields = '__all__'  

# class FavorisForm(forms.ModelForm):
#     class Meta:
#         model = Favoris
#         fields = ['']  

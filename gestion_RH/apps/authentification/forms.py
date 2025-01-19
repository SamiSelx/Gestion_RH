from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder':'Enter your email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
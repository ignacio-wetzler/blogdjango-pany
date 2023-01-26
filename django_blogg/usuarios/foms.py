from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Avatar

class FormularioAlta(UserCreationForm):
    username = UsernameField(label='User')

    class Meta:
        model = User 
        fields = ["username","email","password1","password2"]

class FormModificacionUsuario(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username","email"]

class FormModificacionPerfil(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ["imagen"]

class AvatarForm(forms.Form):
    model = Avatar
    imagen = forms.ImageField(label="imagen")
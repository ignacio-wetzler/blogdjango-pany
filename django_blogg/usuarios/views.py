from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FormularioAlta, FormModificacionUsuario, FormModificacionPerfil, AvatarForm
from .models import Avatar

# Create your views here.

def ObtenerAvatar(request):
    lista = Avatar.objects.filter(user=request.user)

    if len(lista) != 0:
        avatar = lista[0].imagen.url
    else:
        avatar = "/media/avatars/avatarpordefecto.png"

    return avatar

def mostrarAvatar(request):
        return render(request, "blog/mostrarAvatar.html", {"avatar": ObtenerAvatar(request)})

def agregarAvatar(request):
    if request.method=="POST":
        form=AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatar=Avatar(user=request.user, imagen=request.FILES["imagen"])
            avatarViejo=Avatar.objects.filter(user=request.user)
            if len(avatarViejo)>0:
                avatarViejo[0].delete()
            avatar.save()
            return render(request, "blog/agregarAvatar.html", {"mensaje":f"Avatar agregado correctamente"})
        else:
            return render(request, "blog/agregarAvatar.html", {"form": form, "usuario": request.user, "mensaje":"Error al agregar el avatar"})
    else:
        form=AvatarForm()
        return render(request, "blog/agregarAvatar.html", {"form": form, "usuario": request.user})



def alta_usuario(request):
    if request.method == "POST":
        formulario_alta = FormularioAlta(request.POST)
        if formulario_alta.is_valid():
            formulario_alta.save()
            nombre = formulario_alta.cleaned_data.get("username")
            messages.success(request, f"Cuenta creada para {nombre}")
            return redirect("login")
    else:
        formulario_alta = FormularioAlta()
    return render(request, fr"blog/alta.html", {"form" : formulario_alta})

@login_required
def perfil(request):
    if request.method == "POST":
        form_usuario = FormModificacionUsuario(request.POST, instance = request.user)

        if form_usuario.is_valid():
            form_usuario.save()
            messages.success(request, f"Tu cuenta ha sido modficada exitosamente!")
            return redirect("perfil")
        else:
            pass


    else:
        form_usuario = FormModificacionUsuario(instance = request.user)

    context = { "form_usuario": form_usuario, "avatar": ObtenerAvatar(request)}


    return render(request, fr"blog/perfil.html", context)


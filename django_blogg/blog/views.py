from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Post, Comentario
from usuarios.views import ObtenerAvatar
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from usuarios.models import Avatar
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
n = 1

def home(request):

    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)


def about(request):
    f = "media\static\SanAgustin.txt"
    cita = "Liber - ICAPUT 1"
    imagen = "media\static\SanAgustin.jpg"
    return render(request, "blog/about.html", {"titulo": "Sobre Mi!!", "url": f, "cita": cita, "avatar": imagen })


class VistaDeLista(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-fecha"]


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comentarios"] = Comentario.objects.filter(post = self.kwargs["pk"])
        return context


class PostDeleteView(LoginRequiredMixin,  UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class CrearPost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["titulo","contenido"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CrearComentario(LoginRequiredMixin, CreateView, Post):
    model =  Comentario
    fields = ["contc"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs["pk"])
        context["titulo"] = post.titulo
        context["contenido"] = post.contenido
        context["fecha"] = post.fecha
        context["user"] = post.user
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs["pk"])
        return super().form_valid(form)


class ModificarPost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["titulo","contenido"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class ModificarComentario(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comentario
    fields = ["contc"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comentario = self.get_object()
        if self.request.user == comentario.user:
            return True
        return False

class ComentarioDeleteView(LoginRequiredMixin,  UserPassesTestMixin, DeleteView):
    model = Comentario
    success_url = "/"

    def test_func(self):
        comentario = self.get_object()
        if self.request.user == comentario.user:
            return True
        return False
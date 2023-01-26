from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as Usuario
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    titulo = models.CharField(max_length= 30)
    contenido = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("post-detail", kwargs = {"pk": self.pk})

class Comentario(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contc = models.TextField()
    fechc = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-fechc"]

    def __str__(self):
        return self.contenido[0:50]

    def get_absolute_url(self):
        return reverse("post-detail", kwargs = {"pk": self.post.pk})


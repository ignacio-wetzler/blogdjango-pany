from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Avatar(models.Model):
    imagen = models.ImageField(default = "/avatars/avatarpordefecto.png", upload_to = "avatars")
    user = models.OneToOneField(User, on_delete= models.CASCADE)

    def __str__(self):
        return f"Avatar de {self.user.username} - {self.imagen}"
from django.db import models

# Create your models here.
class Contact(models.Model):
    nombre = models.CharField(max_length=90)
    email = models.EmailField(max_length=100)
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre

from django.db import models
import os

def project_image_path(instance, filename):
    # Genera un nombre de archivo basado en el ID del proyecto y la extensión del archivo original
    ext = filename.split('.')[-1]
    new_filename = f'{instance.pk}.{ext}'
    return f'{new_filename}'

class Project(models.Model):
    code = models.CharField(primary_key=True, max_length=4)
    name = models.CharField(max_length=90)
    description = models.CharField(max_length=2000)
    publish = models.BooleanField(default=True)
    image = models.ImageField(upload_to=project_image_path, blank=True, null=True)

    def __str__(self):
        text = "[{0}] {1}"
        t_publish = "On" if self.publish else "Off"
        return text.format(t_publish, self.name)

    def save(self, *args, **kwargs):
        try:
            # Buscar la instancia existente en la base de datos
            existing = Project.objects.get(pk=self.pk)
            # Comprobar si la imagen ha cambiado
            if existing.image != self.image:
                # Eliminar la imagen anterior
                if existing.image:
                    os.remove(existing.image.path)
        except Project.DoesNotExist:
            pass

        super(Project, self).save(*args, **kwargs)

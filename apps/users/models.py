from django.db import models
from django.contrib.auth.models import User
import os

class TrainVersion(models.Model):
    custom_name = models.CharField(max_length=90)
    version = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    trained = models.BooleanField(default=False)
    loss = models.FloatField(null=True, blank=True)  # New field to store the loss value

    def __str__(self):
        return self.custom_name


def train_data_file_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f'{instance.version.pk}.{ext}'
    return os.path.join('train_data', new_filename)

class TrainData(models.Model):
    version = models.ForeignKey(TrainVersion, on_delete=models.CASCADE)
    data = models.FileField(upload_to=train_data_file_path)

    def __str__(self):
        return f"TrainData for Version ID {self.version.pk}"
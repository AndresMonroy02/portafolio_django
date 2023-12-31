from django.db import models

class Contact(models.Model):
    full_name = models.CharField(max_length=90)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.full_name

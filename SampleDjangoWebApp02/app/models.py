"""
Definition of models.
"""

from django.db import models

# Create your models here.
class FileUpload(models.Model):
    files = models.FileField(upload_to = 'files')

class ImageUpload(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to="images")

    def __str__(self):
        return self.title
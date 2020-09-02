from django.db import models

# Create your models here.
# python manage.py makemigrations <app_name>
# python manage.py migrate

class Mapping(models.Model):
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    config = models.TextField()
from django.db import models

# Create your models here.
# python manage.py makemigrations <app_name>
# python manage.py migrate

class Mapping(models.Model):
    PLATFORMS = {
        'a': 'Both (Bluetooth & Infrared)',
        'i': 'Infrared (Lirc)',
        'b': 'Bluetooth (Wiimote)'
     }

    platform = models.CharField(max_length=1, default="a")
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    config = models.TextField()
from django.db import models

# Create your models here.


class Crisis(models.Model):
    crisisID = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

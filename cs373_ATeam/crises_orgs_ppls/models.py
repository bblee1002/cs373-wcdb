from django.db import models

# Create your models here.

class Crisis(models.Model):
    crisisID = models.CharField(max_length=200)
    crisisIDType = models.CharField(max_length=200)

class Organization(models.Model):
    OrgID = models.CharField(max_length=200)
    OrgIDType = models.CharField(max_length=200)

class Person(models.Model):
    PersonID = models.CharField(max_length=200)
    PersonIDType = models.CharField(max_length=200)

class Place(models.Model):
    PlaceID = models.CharField(max_length=200)
    PlaceIDType = models.CharField(max_length=200)


import os
os.environ["DJANGO_SETTINGS_MODULE"] = "cs373_ATeam.settings"
from django.db import models

# Create your models here.


class Crisis(models.Model) :
    crisis_ID         =    models.CharField(max_length=200)
    name              =    models.CharField(max_length=200)
    year              = models.IntegerField(max_length=200)
    person_list       = []
    organization_list = []
    place_list = []

    def add_person(self, person_id) :
    	person_list.append(person_id)

    def add_org(self, org_id) :
    	org_list.append(org_id)

    def add_place(self, place_id) :
    	place_list.append(place_id)


class Person(models.Model) :
    person_ID         =    models.CharField(max_length=200)
    name              =    models.CharField(max_length=200)
    born              = models.IntegerField(max_length=200)
    office            =    models.CharField(max_length=200)
    crisis_list       = []
    organization_list = []

    def add_crisis(self, person_id) :
        crisis_list.append(crisis_id)

    def add_org(self, org_id) :
        org_list.append(org_id)

class Org(models.Model) :
    head_ID     = models.CharField(max_length=200)
    org_ID      = models.CharField(max_length=200)
    name        = models.CharField(max_length=200)
    crisis_list = []
    person_list = []

    def add_person(self, person_id) :
        person_list.append(crisis_id)

    def add_crisis(self, org_id) :
        crisis_list.append(org_id)

class Place(models.Model):
    place_ID = models.CharField(max_length=200)
    name     = models.CharField(max_length=200)

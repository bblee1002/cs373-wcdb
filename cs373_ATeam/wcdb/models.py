from django.db import models

# Create your models here.


class Crisis(models.Model) :
    crisis_ID = models.CharField(max_length=200)
    person_list = []
    organization_list = []
    place_list = []
    #person_ID = models.CharField(max_length=200)
    #org_ID = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    start_date = models.IntegerField(max_length=200)
    end_date = models.IntegerField(max_length=200)

    def add_person(self, person_id) :
    	person_list.append(person_id)

    def add_org(self, org_id) :
    	person_list.append(org_id)

    def add_place(self, place_id) :
    	person_list.append(place_id)


class Person(models.Model) :
    born = models.IntegerField(max_length=200)
    office = models.CharField(max_length=200)
    person_ID = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

class Org(models.Model) :
    head_ID = models.CharField(max_length=200)
    org_ID = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

class Place(models.Model):
    place_ID = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

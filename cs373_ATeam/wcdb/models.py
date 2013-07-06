import os
os.environ["DJANGO_SETTINGS_MODULE"] = "cs373_ATeam.settings"
from django.db import models

# Create your models here.


class Crisis(models.Model) :
    crisis_ID         = models.CharField(max_length=200)
    name              = models.CharField(max_length=200)
    kind              = models.CharField(max_length=200)
    date              = models.CharField(max_length=200)
    time              = models.CharField(max_length=200)
    people            = []
    organizations     = []
    #Li list
    locations         = []
    human_impact      = []
    economic_impact   = []
    resources_needed  = []
    ways_to_help      = []
    #common
    common            = Common()


class Person(models.Model) :
    person_ID         = models.CharField(max_length=200)
    name              = models.CharField(max_length=200)
    kind              = models.CharField(max_length=200)
    location          = models.CharField(max_length=200)
    common            =                         Common()
    crises            = []
    organizations     = []
    

class Org(models.Model) :
    org_ID      = models.CharField(max_length=200)
    head_ID     = models.CharField(max_length=200)
    name        = models.CharField(max_length=200)
    kind        = models.CharField(max_length=200)
    location    = models.CharField(max_length=200)
    crises      = []
    people      = []
    #Li list
    history     = []
    contact     = []
    #Common
    common      = Common()


class Place(models.Model):
    place_ID = models.CharField(max_length=200)
    name     = models.CharField(max_length=200)

#class for the ListType complexType
class Li() :
    #Li
    href
    embed
    text
    #text not in the attributes; not Li
    floating_text

class Common() :
    #Li
    citations      = []
    external_links = []
    images         = []
    videos         = []
    maps           = []
    feeds          = []
    #similar to floating text
    summary

#general method for adding to a list
def list_add(list, id) :
    list.append(id)
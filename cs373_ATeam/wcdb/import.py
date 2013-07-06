import sys
from django.conf import settings
from cs373_ATeam.wcdb.models import Crisis
import xml.etree.ElementTree as ET


#Read XML file
strXML = ""
for line in sys.stdin:
		strXML += line

e_root = ET.fromstring(strXML)

#populate Crisis models
crisis_list = []
populate_crisis(e_root, crisis_list)

#populate Person models
person_list = []
populate_person(e_root, person_list)

#populate Org models
org_list = []
populate_org(e_root, org_list)

#populate Place models
place_list = []
populate_place(e_root, org_list)

def populate_crisis(root, list) :
#Find instances of crises
#and add to a list of crisis objects created by Django
	for crisis in root.iter("Crisis"):
		temp_crisis           =           Crisis()
		temp_crisis.crisis_ID =   crisis.get("ID")
		temp_crisis.name      = crisis.get("Name")
		c_list.append(temp_crisis)

		#populating the year
		crisis.year = int(crisis.find("Year").text)
		#populating people
		for person in crisis.iter("PersonID") :
			temp_crisis.add_person(person.text)
		#populating organizations
		for org in crisis.iter("OrgID") :
			temp_crisis.add_org(org.text)
		#populating places
		for place in crisis.iter("PlaceID") :
			temp_crisis.add_place(place.text)
		#add populated crisis model to list
		list.append(temp_crisis)

def populate_person(root, list) :
#Find instances of person
#and add to a list of crisis objects created by Django
	for person in root.iter("Person"):
		temp_person             =                     Person()
		temp_person.person_ID   =             person.get("ID")
		temp_person.name        =           person.get("Name")
		temp_person.born        = int(person.find("Born").text)
		temp_person.office      =    person.find("Office").text

		for org in person.iter("OrgID") :
				temp_person.add_org(org.text)
		list.append(temp_person)

def populate_org(root, list) :
	for org in root.iter("Organization")
		temp_org         =                Org()
		temp_org.org_ID  =        org.get("ID")
		temp_org.head_ID = org.get("OrgHeadID")
		temp_org.name    =      org.get("Name")

		for person in org.iter("PersonID") :
			temp_org.add_person(person.text)


		list.append(temp_org)

def populate_place(root, list) :
	for place in root.iter("Place") :
		temp_place          = Place()
		temp_place.place_ID = place.get("ID")
		temp_place.name     = place.get("Name")

		list.append(temp_place)

#function for validating the file
def validate(file) :
	name = file.name
	if name[-4:] == ".xml"
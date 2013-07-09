import sys
from genxmlif import GenXmlIfError
from minixsv import pyxsval
from django.conf import settings
from models import Crisis, Person, Org, Li, Common, list_add
import xml.etree.ElementTree as ET

def populate_models(file) :

	#Read XML file
	strXML = ""
	for line in file:
			strXML += line

	e_root = ET.fromstring(strXML)

	#populate Crisis models
	crises = []
	populate_crisis(e_root, crises)

	#populate Person models
	people = []
	populate_person(e_root, people)

	#populate Org models
	organizations    = []
	populate_org(e_root, organizations)


def populate_crisis(root, list) :
#Find instances of crises
#and add to a list of crisis objects created by Django
	for crisis in root.findall("Crisis"):
		temp_crisis           =                 Crisis()
		temp_crisis.crisis_ID =         crisis.get("ID")
		temp_crisis.name      =       crisis.get("Name")
		temp_crisis.kind      = crisis.find("Kind").text
		temp_crisis.date      = crisis.find("Date").text
		crisis.time           = crisis.find("Time").text
		#populating people
		for person in crisis.iter("Person") :
			list_add(temp_crisis.people, person.get("ID"))
		#populating organizations
		for org in crisis.iter("Org") :
			list_add(temp_crisis.organizations, org.get("ID"))

		for location in crisis.find("Locations") :
			temp_li = Li()
			temp_li.populate(location)
			list_add(temp_crisis.locations, temp_li)

		for human_impact in crisis.find("HumanImpact") :
			temp_li = Li()
			temp_li.populate(human_impact)
			list_add(temp_crisis.human_impact, temp_li)

		for economic_impact in crisis.find("EconomicImpact") :
			temp_li = Li()
			temp_li.populate(economic_impact)
			list_add(temp_crisis.economic_impact, temp_li)

		for resource in crisis.find("ResourcesNeeded") :
			temp_li = Li()
			temp_li.populate(resource)
			list_add(temp_crisis.resources_needed, temp_li)

		for help in crisis.find("WaysToHelp") :
			temp_li                  =             Li()
			temp_li.populate(help)
			list_add(temp_crisis.ways_to_help, temp_li)

		#populating common fields
		temp_crisis.common.populate(crisis.find("Common"))


		#add populated crisis model to list
		list.append(temp_crisis)

def populate_person(root, list) :
#Find instances of person
#and add to a list of crisis objects created by Django
	for person in root.findall("Person"):
		temp_person             =                     Person()
		temp_person.person_ID   =             person.get("ID")
		temp_person.name        =           person.get("Name")
		temp_person.kind        =     person.find("Kind").text
		temp_person.location    = person.find("Location").text

		for crisis in person.iter("Crisis") :
				list_add(temp_person.crises, crisis.get("ID"))

		for org in person.iter("Org") :
				list_add(temp_person.organizations, org.get("ID"))
		list.append(temp_person)

def populate_org(root, list) :
	for org in root.findall("Organization") :
		temp_org         =                 Org()
		temp_org.org_ID  =         org.get("ID")
		temp_org.name    =       org.get("Name")
		temp_org.kind    = org.find("Kind").text

		for crisis in org.iter("Crisis") :
				list_add(temp_org.crises, crisis.get("ID"))

		for person in org.iter("Person") :
			list_add(temp_org.people, person.get("ID"))

		for history in org.find("History") :
			temp_li = Li()
			temp_li.populate(history)
			list_add(temp_org.history, temp_li)

		for contact in org.find("ContactInfo") :
			temp_li = Li()
			temp_li.populate(contact)
			list_add(temp_org.contact, temp_li)

		#populating common fields
		temp_org.common.populate(org.find("Common"))

		list.append(temp_org)

#function for validating the file
def validate(file_in) :
	name = str(file_in.name)
	if name[-4:] != ".xml" and name[-4:] != ".XML" :
		return False
	xsd = open('wcdb/WorldCrises.xsd.xml', 'r')
	xmlFile = open('wcdb/temp.xml', 'w')
	xmlFile.write(file_in.read())
	xmlFile = open('wcdb/temp.xml', 'r')
	try:
		psvi = pyxsval.parseAndValidate("wcdb/temp.xml", "wcdb/WorldCrises.xsd.xml",
			xmlIfClass=pyxsval.XMLIF_ELEMENTTREE)
	except pyxsval.XsvalError, e:
		print e
		print 'Validation aborted.'
		return False
	except GenXmlIfError, e:
		print e
		print 'Parsing aborted.'
		return False
	except Exception, e:
		# catch all
		print e
		return False
	#handle invalid case
	return True

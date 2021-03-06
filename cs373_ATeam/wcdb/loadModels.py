import sys
from genxmlif import GenXmlIfError
from minixsv import pyxsval
from django.conf import settings
from models import Crisis, Person, Org, Li, Common, Relations, populate_li
import xml.etree.ElementTree as ET

"""
File imports an xml file, sent in by the user from the website, and populates Django models
using the information from the file.
"""

def populate_models(tree) :
	"""
	Function expects an element tree as a parameter. Main function of the file that calls
	populate_crisis, populate_org, and populate_person. Returns a dictionary where the keys
	are the type of model and the values are lists of instances of the models populated by 
	this funciton.

	@type  tree: ElementTree
	@param tree: the XML file, uploaded by the user, parsed into an ElementTree
	@rtype:      N/A
	@return:     function does not return
	"""
	e_root = tree.getroot()
	populate_crisis(e_root)
	populate_person(e_root)
	populate_org(e_root)

def populate_common(node, modl_id, model_instance):
	"""
	Searches through node's tree for a common node and calls common's populate method
	on it. 

	@type  node:           Element
	@param node:           a node in the ElementTree passed in to populate_models()
	@type  modl_id:        string
	@param modl_id:        the idref of the model the common instance maps to
	@type  model_instance: element
	@param model_instance: a node in the ElementTree passed in to populate_models()
	@rtype:                N/A
	@return:               function does not return
	"""
	found_common = node.find('Common')
	if found_common is not None:
		common = Common()
		common.populate(found_common, modl_id)
		found_summary = found_common.find("Summary")

		if found_summary is not None and found_summary is not "" :
			if found_summary.text is not None and found_summary.text is not "" :
				model_instance.common_summary = found_summary.text

def populate_crisis(root) :
	"""
	Finds instances of Crisis in root's tree and saves them to the database

	@type root:  Element
	@param root: root of the ElementTree passed in to populate_models()
	@rtype:      N/A
	@return:     function does not return
	"""
	for crisis in root.findall("Crisis"):
		temp_crisis           =                 Crisis()
		temp_crisis.crisis_ID =         crisis.get("ID")
		temp_crisis.name      =       crisis.get("Name")
		
		if crisis.find("Kind") is not None :
			temp_crisis.kind      = crisis.find("Kind").text
		if crisis.find("Date") is not None :
			temp_crisis.date      = crisis.find("Date").text
		if crisis.find("Time") is not None :
			temp_crisis.time      = crisis.find("Time").text
		#populating people
		for person in crisis.iter("Person") or [] :
			temp_relations = Relations()
			check = Relations.objects.filter(crisis_ID = crisis.get("ID"), person_ID = person.get("ID"))
			if len(check) == 0:
				temp_relations.populate(c_id = crisis.get("ID"), p_id = person.get("ID"))
				temp_relations.save()
		#populating organizations
		for org in crisis.iter("Org") or [] :
			temp_relations = Relations()
			check = Relations.objects.filter(crisis_ID = crisis.get("ID"), org_ID = org.get("ID"))
			if len(check) == 0:
				temp_relations.populate(c_id = crisis.get("ID"), o_id = org.get("ID"))
				temp_relations.save()

		populate_li(crisis, crisis.get("ID"), "Locations")
		populate_li(crisis, crisis.get("ID"), "HumanImpact")
		populate_li(crisis, crisis.get("ID"), "EconomicImpact")
		populate_li(crisis, crisis.get("ID"), "ResourcesNeeded")
		populate_li(crisis, crisis.get("ID"), "WaysToHelp")

		populate_common(crisis, crisis.get("ID"), temp_crisis)
		temp_crisis.save()



def populate_person(root) :
	"""
	Finds instances of Person in root's tree and saves them to the database

	@type root:  Element
	@param root: root of the ElementTree passed in to populate_models()
	@rtype:      N/A
	@return:     function does not return
	"""
	for person in root.findall("Person"):
		temp_person             =                     Person()
		temp_person.person_ID   =             person.get("ID")
		temp_person.name        =           person.get("Name")

		if person.find("Kind") is not None :
			temp_person.kind        =     person.find("Kind").text
		if person.find("Location") is not None :
			temp_person.location    = person.find("Location").text

		for crisis in person.iter("Crisis") :
			temp_relations = Relations()
			check = Relations.objects.filter(crisis_ID = crisis.get("ID"), person_ID = person.get("ID"))
			if len(check) == 0:
				temp_relations.populate(c_id = crisis.get("ID"), p_id = person.get("ID"))
				temp_relations.save()

		for org in person.iter("Org") :
			temp_relations = Relations()
			check = Relations.objects.filter(org_ID = org.get("ID"), person_ID = person.get("ID"))
			if len(check) == 0:
				temp_relations.populate(p_id = person.get("ID"), o_id = org.get("ID"))
				temp_relations.save()

		populate_common(person, person.get("ID"), temp_person)
		temp_person.save()

def populate_org(root) :
	"""
	Finds instances of Org in root's tree and saves them to the database

	@type root:  Element
	@param root: root of the ElementTree passed in to populate_models()
	@rtype:      N/A
	@return:     function does not return
	"""
	for org in root.findall("Organization") :
		temp_org          =                     Org()
		temp_org.org_ID   =             org.get("ID")
		temp_org.name     =           org.get("Name")
		if org.find("Kind") is not None :
			temp_org.kind     =     org.find("Kind").text
		if org.find("Location") is not None :
			temp_org.location = org.find("Location").text

		for crisis in org.iter("Crisis") :
			temp_relations = Relations()
			check = Relations.objects.filter(crisis_ID = crisis.get("ID"), org_ID = org.get("ID"))
			if len(check) == 0:
				temp_relations.populate(c_id = crisis.get("ID"), o_id = org.get("ID"))
				temp_relations.save()

		for person in org.iter("Person") :
			temp_relations = Relations()
			check = Relations.objects.filter(org_ID = org.get("ID"), person_ID = person.get("ID"))
			if len(check) == 0:
				temp_relations.populate(p_id = person.get("ID"), o_id = org.get("ID"))
				temp_relations.save()

		populate_li(org, org.get("ID"), "History")
		populate_li(org, org.get("ID"), "ContactInfo")

		populate_common(org, org.get("ID"), temp_org)
		temp_org.save()

def validate(file_in) :
	"""
	Function expects a file as a parameter. Checks if file is a valid xml file.
	Returns False if not, and an element tree built from the file if it is valid.

	@type file_in:  File
	@param file_in: file uploaded by the user, passed by views.py
	@rtype:         Boolean or ElementTree
	@return:        Returns False if the filen is invalid XML, or an element tree 
	                built from the file if it is valid.
	"""
	name = str(file_in.name)
	if name[-4:] != ".xml" and name[-4:] != ".XML" :
		return False
	xsd = open('wcdb/WorldCrises.xsd.xml', 'r')
	xmlFile = open('wcdb/temp.xml', 'w')
	xmlFile.write(file_in.read())
	xmlFile = open('wcdb/temp.xml', 'r')
	try:
		psvi = pyxsval.parseAndValidate("wcdb/temp.xml",
			"wcdb/WorldCrises.xsd.xml", xmlIfClass=pyxsval.XMLIF_ELEMENTTREE)
		tree = psvi.getTree()
	except pyxsval.XsvalError, e:
		return 'Validation aborted. ' + str(e)
	except GenXmlIfError, e:
		return 'Parsing aborted. ' + str(e)
	except Exception as e:
		# catch all
		return 'Exception. ' + str(e)
	#handle invalid case
	return tree
